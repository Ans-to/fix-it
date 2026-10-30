#!/usr/bin/env python3
"""Small deterministic SVG example renderer for the director vector v1 profile.

Requires jsonschema 4.x; does not rasterize, encode, shape text or mix audio.
"""
import argparse
import base64
import hashlib
import html
import json
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit('jsonschema is required; install code-video/requirements.txt; validation NOT CHECKED')

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / 'manifest.schema.json').read_text(encoding='utf-8'))


def load(path):
    def bad_constant(value): raise ValueError('non-finite JSON number: '+value)
    def unique_pairs(pairs):
        result={}
        for key,value in pairs:
            if key in result: raise ValueError('duplicate JSON key: '+key)
            result[key]=value
        return result
    p = Path(path)
    return json.loads(p.read_text(encoding='utf-8'), parse_constant=bad_constant, object_pairs_hook=unique_pairs)


def validate(m, folder):
    errors = [f'{"/".join(map(str,e.absolute_path))}: {e.message}'
              for e in sorted(Draft202012Validator(SCHEMA).iter_errors(m), key=lambda e: list(map(str,e.absolute_path)))]
    if errors: return errors
    def finite(v):
        if isinstance(v,float): return math.isfinite(v)
        if isinstance(v,list): return all(finite(x) for x in v)
        if isinstance(v,dict): return all(finite(x) for x in v.values())
        return True
    if not finite(m): errors.append('non-finite number')
    fps = m['timing']['fps']; dur = m['timing']['duration_seconds']
    rational = Fraction(fps['numerator'],fps['denominator'])*Fraction(dur['numerator'],dur['denominator'])
    frames = (2*rational.numerator+rational.denominator)//(2*rational.denominator)
    n = m['timing']['total_frames']
    if n != frames: errors.append('total_frames differs from round-half-up(duration * fps)')
    if m['purpose']=='production' and (fps['status']!='CONFIRMED' or dur['status']!='CONFIRMED'):
        errors.append('production requires CONFIRMED fps and duration; use illustrative otherwise')
    cursor=0; scene_ids=set()
    for scene in m['scenes']:
        if scene['id'] in scene_ids: errors.append('duplicate scene id '+scene['id'])
        scene_ids.add(scene['id'])
        if scene['start']!=cursor or scene['end']<=scene['start']: errors.append('scenes must cover timeline consecutively')
        cursor=scene['end']
    if cursor!=n: errors.append('scene coverage does not end at total_frames')
    assets={}
    for a in m['asset_policy']['assets']:
        if a['id'] in assets: errors.append('duplicate asset id '+a['id'])
        assets[a['id']]=a
        if a['kind'] not in m['asset_policy']['allowed']: errors.append('disallowed asset '+a['id'])
        p=Path(a['path']); root=Path(folder).resolve(); resolved=(root/p).resolve()
        if p.is_absolute() or '..' in p.parts or not resolved.is_relative_to(root):
            errors.append('unsafe asset path '+a['path']); continue
        if p.suffix.lower() not in ('.ttf','.otf','.woff','.woff2'):
            errors.append('unsupported font extension '+a['path']); continue
        try: digest=hashlib.sha256(resolved.read_bytes()).hexdigest()
        except OSError: errors.append('asset unavailable '+a['path']); continue
        if digest!=a['sha256']: errors.append('asset hash mismatch '+a['path'])
    ids=set()
    for o in m['objects']:
        if o['id'] in ids: errors.append('duplicate object id '+o['id'])
        ids.add(o['id']); a,b=o['visible']
        if not 0<=a<b<=n: errors.append('invalid visibility for '+o['id'])
        if o['type']=='text':
            if o['geometry']['font_asset'] not in assets:
                errors.append('text references missing font asset for '+o['id'])
            if any(not (ord(ch) in (9,10,13) or 0x20<=ord(ch)<=0xD7FF or 0xE000<=ord(ch)<=0xFFFD or 0x10000<=ord(ch)<=0x10FFFF) for ch in o['geometry']['text']):
                errors.append('text contains an invalid XML character for '+o['id'])
        groups={}
        for anim in o['animations']:
            start,end=anim['start'],anim['end']
            if not a<=start<end<b: errors.append('animation outside visible range or has no duration for '+o['id'])
            if anim['property']=='opacity' and not all(0<=anim[k]<=1 for k in ('from','to')):
                errors.append('opacity animation outside [0,1] for '+o['id'])
            groups.setdefault(anim['property'],[]).append((start,end))
        for prop,ranges in groups.items():
            ranges.sort()
            if any(left[1]>=right[0] for left,right in zip(ranges,ranges[1:])):
                errors.append('overlapping animation intervals for '+o['id']+'/'+prop)
    return errors


def number(x):
    # Stable SVG decimal representation; geometry calculations remain unrounded.
    if abs(x)<0.0000005: x=0
    return f'{x:.6f}'.rstrip('0').rstrip('.') or '0'


def values(o,frame):
    result={'translate_x':0.0,'translate_y':0.0,'opacity':o['style']['opacity']}
    for prop in result:
        seq=sorted((a for a in o['animations'] if a['property']==prop),key=lambda a:a['start'])
        if not seq: continue
        # Before first event hold its from; between/after events hold the last to.
        val=seq[0]['from']
        for a in seq:
            if frame<a['start']: break
            if frame>=a['end']: val=a['to']; continue
            t=(frame-a['start'])/(a['end']-a['start'])
            if a['easing']=='smoothstep': t=t*t*(3-2*t)
            elif a['easing']=='step': t=0
            val=a['from']+(a['to']-a['from'])*t
            break
        result[prop]=val
    return result


def render(m,frame,folder):
    if not 0<=frame<m['timing']['total_frames']: raise ValueError('frame out of range')
    c=m['canvas']; camera=m['camera']; ax,ay=camera['anchor']; ox,oy=camera['offset']; scale=camera['scale']
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{c["width"]}" height="{c["height"]}" viewBox="0 0 {c["width"]} {c["height"]}">']
    for a in sorted(m['asset_policy']['assets'],key=lambda x:x['id']):
        suffix=Path(a['path']).suffix.lower(); mime={'.ttf':'font/ttf','.otf':'font/otf','.woff':'font/woff','.woff2':'font/woff2'}[suffix]
        data=base64.b64encode((Path(folder)/a['path']).read_bytes()).decode('ascii')
        svg.append(f'<style>@font-face{{font-family:{a["id"]};src:url(data:{mime};base64,{data})}}</style>')
    svg.append(f'<rect x="0" y="0" width="{c["width"]}" height="{c["height"]}" fill="{c["background"]}"/>')
    for o in sorted(m['objects'],key=lambda o:(o['z'],o['id'])):
        if not o['visible'][0]<=frame<o['visible'][1]: continue
        v=values(o,frame); tx,ty=v['translate_x'],v['translate_y']
        transform=f'translate({number(tx)} {number(ty)})'
        if o['space']=='world':
            transform=(f'translate({number(ox)} {number(oy)}) translate({number(ax)} {number(ay)}) '
                       f'scale({number(scale)}) translate({number(-ax)} {number(-ay)}) '+transform)
        s=o['style']; fill=s['fill'] or 'none'; stroke=s['stroke'] or 'none'; g=o['geometry']
        style=f'fill="{fill}" stroke="{stroke}" stroke-width="{number(s["stroke_width"])}" opacity="{number(v["opacity"])}"'
        if o['type']=='rect': attrs=f'x="{number(g["x"])}" y="{number(g["y"])}" width="{number(g["width"])}" height="{number(g["height"])}"'; element=f'<rect {attrs} {style}/>'
        elif o['type']=='circle': attrs=f'cx="{number(g["cx"])}" cy="{number(g["cy"])}" r="{number(g["radius"])}"'; element=f'<circle {attrs} {style}/>'
        elif o['type']=='line': attrs=' '.join(f'{k}="{number(g[k])}"' for k in ('x1','y1','x2','y2')); element=f'<line {attrs} {style}/>'
        else:
            txt=html.escape(g['text'],quote=False)
            element=f'<text x="{number(g["x"])}" y="{number(g["y"])}" font-family="{g["font_asset"]}" font-size="{number(g["font_size"])}" {style}>{txt}</text>'
        svg.append(f'<g id="{o["id"]}" transform="{transform}">{element}</g>')
    svg.append('</svg>')
    return ('\n'.join(svg)+'\n').encode('utf-8')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest',type=Path);parser.add_argument('--frame',type=int,required=True);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--force',action='store_true',help='replace an existing output only with the user’s permission')
    a=parser.parse_args()
    try:
        m=load(a.manifest); errors=validate(m,a.manifest.parent)
        if errors: raise ValueError('\n'.join(errors))
        result=render(m,a.frame,a.manifest.parent)
        with a.output.open('wb' if a.force else 'xb') as output: output.write(result)
    except (ValueError,OSError) as e:
        print('ERROR: '+str(e),file=sys.stderr); return 1
    return 0

if __name__=='__main__': sys.exit(main())
