#!/usr/bin/env python3
"""Scoped QA for the v1 SVG reference implementation; prints a JSON report."""
import argparse
import json
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from vector_profile import load,validate,render,values


def box_at(o,frame,camera):
    g=o['geometry']; v=values(o,frame); kind=o['type']
    if kind=='text': return None # no text shaper/metrics here
    if kind=='rect': box=[g['x'],g['y'],g['x']+g['width'],g['y']+g['height']]
    elif kind=='circle': box=[g['cx']-g['radius'],g['cy']-g['radius'],g['cx']+g['radius'],g['cy']+g['radius']]
    else: box=[min(g['x1'],g['x2']),min(g['y1'],g['y2']),max(g['x1'],g['x2']),max(g['y1'],g['y2'])]
    # Conservative stroke expansion. World camera is a uniform, positive scale.
    pad=o['style']['stroke_width']/2 if o['style']['stroke'] else 0
    box=[box[0]-pad,box[1]-pad,box[2]+pad,box[3]+pad]
    dx,dy=v['translate_x'],v['translate_y']
    box=[box[0]+dx,box[1]+dy,box[2]+dx,box[3]+dy]
    if o['space']=='world':
        s=camera['scale']; ax,ay=camera['anchor']; ox,oy=camera['offset']
        box=[(box[0]-ax)*s+ax+ox,(box[1]-ay)*s+ay+oy,(box[2]-ax)*s+ax+ox,(box[3]-ay)*s+ay+oy]
    return box


def report(m,folder,limit=10000):
    errors=validate(m,folder)
    if errors: return {'manifest_validation':{'status':'FAIL','errors':errors},'overall':'FAIL'}
    n=m['timing']['total_frames']; sample=sorted(set([0,n//2,n-1])); outputs={}
    try:
        for f in sample: outputs[f]=render(m,f,folder); ET.fromstring(outputs[f])
        repeat={f:render(m,f,folder) for f in reversed(sample)}
        deterministic=outputs==repeat
    except Exception as e:
        return {'manifest_validation':{'status':'PASS','scope':'schema, timeline, assets and semantic validation'},'sample_render':{'status':'FAIL','error':str(e)},'overall':'FAIL'}
    frames=list(range(n)) if n<=limit else sample
    failures=[]; text_skipped=set(); checked=0; w=m['canvas']['width'];h=m['canvas']['height']
    for f in frames:
        for o in m['objects']:
            if not o['visible'][0]<=f<o['visible'][1]: continue
            b=box_at(o,f,m['camera'])
            if b is None: text_skipped.add(o['id']); continue
            checked+=1
            if b[0]<0 or b[1]<0 or b[2]>w or b[3]>h: failures.append({'frame':f,'object':o['id'],'box':b})
    geometry='FAIL' if failures else ('NOT CHECKED' if not checked else ('PARTIAL' if text_skipped or len(frames)!=n else 'PASS'))
    if not deterministic or failures: overall='FAIL'
    else: overall='PARTIAL' # core tests are intentionally missing
    return {'manifest_validation':{'status':'PASS','scope':'schema, scene timeline, animation intervals, approved timing if production, and declared asset hashes'},
            'sample_seek_repeat':{'status':'PASS' if deterministic else 'FAIL','frames':sample,'scope':'SVG bytes for selected frames rendered twice in reverse order, same environment'},
            'all_frame_seekability':{'status':'PARTIAL' if deterministic else 'FAIL','frames_checked':sample,'reason':'two sampled seek orders in one environment are not an exhaustive determinism proof'},
            'analytic_shape_canvas_bounds':{'status':geometry,'frames_checked':len(frames),'total_frames':n,'object_frame_checks':checked,'skipped_text':sorted(text_skipped),'failures':failures[:100], 'scope':'conservative rect/circle/line bounds and stroke only; no mask or text shaping'},
            'overlap_containment_connector_contrast_caption':{'status':'NOT CHECKED','reason':'requires project-specific measured geometry/relationships; see measured_checks.py'},
            'raster_playback_audio_platform_accessibility':{'status':'NOT CHECKED','reason':'SVG bytes are not a final video, platform preview, audio or accessibility review'},
            'overall':overall}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest',type=Path);p.add_argument('--max-frames',type=int,default=10000)
    a=p.parse_args()
    if a.max_frames<1: p.error('--max-frames must be positive')
    try:r=report(load(a.manifest),a.manifest.parent,a.max_frames)
    except (ValueError,OSError) as e:
        r={'manifest_validation':{'status':'FAIL','error':str(e)},'overall':'FAIL'}
    print(json.dumps(r,indent=2)); return 1 if r['overall']=='FAIL' else 0

if __name__=='__main__':sys.exit(main())
