#!/usr/bin/env python3
"""Test the proposed visual plan. Pillow required; no external visual assets used."""
import hashlib,json,math,re
from functools import lru_cache
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
p=json.loads((ROOT/'visual-plan.json').read_text()); C=p['format']; W,H,FPS,N=(C[k] for k in ('width','height','fps','frames')); colors=p['colors']; FONT=p['font']['tested_path']
@lru_cache(None)
def font(size):return ImageFont.truetype(FONT,size)
@lru_cache(None)
def relbox(t,size):return ImageDraw.Draw(Image.new('RGB',(1,1))).textbbox((0,0),t,font=font(size),anchor='mm')
def rgba(c):
 c=colors[c].lstrip('#');return tuple(int(c[i:i+2],16) for i in (0,2,4))
def smooth(x):
 u=max(0,min(1,x));return u*u*(3-2*u)
def overlaps(a,b):return a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]
def scene_at(f):return next(s for s in p['scenes'] if s['start']<=f<s['end'])
def state(s,f,o):
 t=f-s['start'];a=smooth((t-o['delay'])/18)
 if 'fade_out' in o:
  a0,b0=o['fade_out'];a*=1-smooth((t-a0)/(b0-a0))
 z=1 if o['group']=='screen' else s['camera']['zoom_start']+(s['camera']['zoom_end']-s['camera']['zoom_start'])*smooth(t/(s['end']-s['start']-1))
 def xy(x,y):return (x,y) if o['group']=='screen' else (540+(x-540)*z,960+(y-960)*z)
 xx=None
 if 'move_x' in o:
  m=o['move_x'];xx=m['from']+(m['to']-m['from'])*smooth((t-m['local_start'])/(m['local_end']-m['local_start']))
 return a,z,xy,xx
def bounds(s,f,o):
 a,z,xy,xx=state(s,f,o);k=o['kind']
 if k=='text':
  x,y=xy(xx if xx is not None else o['x'],o['y']); b=relbox(o['text'],round(o['size']*z));return (round(x)+b[0],round(y)+b[1],round(x)+b[2],round(y)+b[3])
 if k=='circle':
  x,y=xy(xx if xx is not None else o['x'],o['y']);r=o['radius']*z;return (x-r,y-r,x+r,y+r)
 if k=='rect':
  x1,y1=xy(o['x'],o['y']);x2,y2=xy(o['x']+o['w'],o['y']+o['h']);return (x1,y1,x2,y2)
 x1,y1=xy(o['x1'],o['y1']);x2,y2=xy(o['x2'],o['y2']);return (min(x1,x2),min(y1,y2),max(x1,x2),max(y1,y2))
def point(s,f,o):
 a,z,xy,xx=state(s,f,o);return xy(xx if xx is not None else o['x'],o['y'])
def circle_contains(box,center,r):
 return all(math.dist((x,y),center)<=r for x in (box[0],box[2]) for y in (box[1],box[3]))
def contrast(fg,bg):
 def lum(rgb):
  def ch(x):
   x=x/255;return x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4
  return .2126*ch(rgb[0])+.7152*ch(rgb[1])+.0722*ch(rgb[2])
 a,b=sorted((lum(rgba(fg)),lum(rgba(bg))),reverse=True);return round((a+.05)/(b+.05),2)

def render(f):
 s=scene_at(f);im=Image.new('RGBA',(W,H),rgba('night')+(255,))
 for o in sorted(s['objects'],key=lambda o:o['group']=='screen'):
  a,z,xy,xx=state(s,f,o)
  if a<=0:continue
  layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer);alpha=round(a*255)
  def c(name):return rgba(name)+(alpha,)
  if o['kind']=='text':
   x,y=xy(xx if xx is not None else o['x'],o['y']);d.text((round(x),round(y)),o['text'],font=font(round(o['size']*z)),fill=c(o['color']),anchor='mm')
  elif o['kind']=='circle':d.ellipse(bounds(s,f,o),fill=c(o['fill']),outline=c(o['stroke']),width=round(o['stroke_width']*z))
  elif o['kind']=='rect':d.rounded_rectangle(bounds(s,f,o),radius=round(o['radius']*z),fill=c(o['fill']),outline=c(o['stroke']),width=round(o['stroke_width']*z))
  else:
   a1=xy(o['x1'],o['y1']);a2=xy(o['x2'],o['y2']);d.line((*a1,*a2),fill=c(o['color']),width=round(o['stroke_width']*z))
  im=Image.alpha_composite(im,layer)
 cue=next(c for c in s['captions'] if c['start']<=f<c['end']);d=ImageDraw.Draw(im);d.rounded_rectangle((70,1510,1010,1690),radius=22,fill=rgba('panel')+(255,))
 ys=[1600] if len(cue['lines'])==1 else [1568,1635]
 for y,line in zip(ys,cue['lines']):d.text((540,y),line,font=font(42),fill=rgba('ivory')+(255,),anchor='mm')
 return im.convert('RGB')

assert (W,H,FPS,N)==(1080,1920,30,1800)
assert len(p['scenes'])==8
cursor=0;count=0;rates={};pairs=set();issues=[]
for s in p['scenes']:
 assert s['start']==cursor and s['end']>cursor;cursor=s['end']
 assert (s['camera']['yaw'],s['camera']['pitch'],s['camera']['roll'])==(0,0,0)
 assert s['camera']['screen_center']==s['camera']['zoom_anchor']==[540,960]
 objs={o['id']:o for o in s['objects']};assert len(objs)==len(s['objects'])
 assert objs['heading']['group']==objs['subheading']['group']=='screen'
 assert all(o['kind'] in ('text','circle','rect','line') for o in s['objects'])
 assert all(o['group'] in ('screen','world') for o in s['objects'])
 cues=s['captions'];assert cues[0]['start']==s['start'] and cues[-1]['end']==s['end']
 assert all(a['end']==b['start'] for a,b in zip(cues,cues[1:]))
 assert ' '.join(line for cue in cues for line in cue['lines'])==s['voiceover']
 assert all(1<=len(cue['lines'])<=2 for cue in cues)
 tokens=len(re.findall(r"[\w]+(?:['’][\w]+)?",s['voiceover']));count+=tokens;rates[s['id']]=round(tokens*60*FPS/(s['end']-s['start']),1)
 for o in s['objects']:
  if o['kind']=='text':
   pairs.add((o['color'],o['background']))
   if 'container' in o:
    assert objs[o['container']]['fill']==o['background'],(s['id'],o['id'],'background mismatch')
   else:assert o['background']=='night'
pairs.add(('ivory','panel')) # caption foreground and panel
assert cursor==N
# Check the opening's token actually touches both parties at the stated endpoints.
s=p['scenes'][0];o={ob['id']:ob for ob in s['objects']}
for f,node_id in ((18,'country_a'),(120,'country_b')):
 node=o[node_id];token=o['token'];z=state(s,f,node)[1];d=math.dist(point(s,f,node),point(s,f,token));assert abs(d-(node['radius']+token['radius'])*z)<1e-8
# Each network link enters its intended node; endpoints and nodes share one camera and no offset.
s=next(s for s in p['scenes'] if s['id']=='07_network');o={ob['id']:ob for ob in s['objects']}
for lid,a,b in [('hub_left','hub','left_node'),('hub_right','hub','right_node'),('existing_peers','left_node','right_node'),('new_to_left','new_node','left_node'),('new_to_right','new_node','right_node'),('new_to_hub','hub','new_node')]:
 l=o[lid];aa=o[a];bb=o[b]
 assert math.dist((l['x1'],l['y1']),(aa['x'],aa['y']))<=aa['radius']
 assert math.dist((l['x2'],l['y2']),(bb['x'],bb['y']))<=bb['radius']
assert o['new_node']['delay']>o['left_node']['delay']
assert all(o[key]['delay']==o['new_node']['delay'] for key in ('new_to_left','new_to_right','new_to_hub'))
assert 'foreign central banks' in next(s for s in p['scenes'] if s['id']=='04_gold')['voiceover'].lower()
assert 'FOREIGN CENTRAL BANKS' in {x.get('text') for x in next(s for s in p['scenes'] if s['id']=='04_gold')['objects']}
assert 'not the only one' in p['scenes'][1]['voiceover'].lower()
assert 'two countries' in p['scenes'][-1]['voiceover'].lower()
assert all(x in p['restrictions'][0].lower() for x in ('images','video'))
for f in range(N):
 s=scene_at(f);objs={o['id']:o for o in s['objects']};texts=[]
 for o in s['objects']:
  a,z,xy,xx=state(s,f,o)
  if a<=0:continue
  b=bounds(s,f,o)
  if b[0]<35 or b[2]>W-35 or b[1]<90 or b[3]>1450:issues.append(f'{f}: {o["id"]} out of planned bounds {b}')
  if o['kind']=='text':
   for name,other in texts:
    if overlaps(b,other):issues.append(f'{f}: text overlap {name} / {o["id"]}')
   texts.append((o['id'],b))
   if 'container' in o:
    parent=objs[o['container']];parent_alpha,sz,_,_=state(s,f,parent)
    if parent_alpha>0:
     if parent['kind']=='rect':
      r=bounds(s,f,parent)
      if b[0]<r[0]+8 or b[1]<r[1]+8 or b[2]>r[2]-8 or b[3]>r[3]-8:issues.append(f'{f}: {o["id"]} outside rectangle {parent["id"]}')
     else:
      radius=(parent['radius']-parent['stroke_width']-3)*sz
      if not circle_contains(b,point(s,f,parent),radius):issues.append(f'{f}: {o["id"]} outside circle {parent["id"]}')
 cue=[x for x in s['captions'] if x['start']<=f<x['end']]
 if len(cue)!=1:issues.append(f'{f}: caption coverage')
 else:
  ys=[1600] if len(cue[0]['lines'])==1 else [1568,1635]
  for y,ln in zip(ys,cue[0]['lines']):
   b=relbox(ln,42);bb=(540+b[0],y+b[1],540+b[2],y+b[3])
   if bb[0]<100 or bb[2]>980 or bb[1]<1510 or bb[3]>1690:issues.append(f'{f}: caption outside panel {bb}')
ratios={f'{a} on {b}':contrast(a,b) for a,b in sorted(pairs)}
assert min(ratios.values())>=4.5,ratios
print('Frame coverage:',cursor,'/',N,'; 60 seconds at 30 fps')
print('All-frame selected text/shape bounds, circle+rectangle containment, captions:',len(issues),'issues')
print('Nominal fully opaque pairs:',ratios)
print('Word tokens:',count,'; approximate per-scene rates:',rates)
if issues:
 print('\n'.join(issues[:25]));raise SystemExit(1)
frames=[s['start']+(s['end']-s['start'])//2 for s in p['scenes']]
sheet=Image.new('RGB',(216*4,(384+28)*2),'white');d=ImageDraw.Draw(sheet)
for i,(s,f) in enumerate(zip(p['scenes'],frames)):
 x=i%4*216;y=i//4*412;d.text((x+4,y+5),f'{s["id"]} / frame {f}',fill='black');sheet.paste(render(f).resize((216,384)),(x,y+28))
sheet.save(ROOT/'qa-contact-sheet.png')
result={'frames_checked':N,'selected_geometry_issues':0,'estimated_word_tokens':count,'estimated_tokens_per_minute':rates,'nominal_text_background_pairs':ratios,'preview_frames':frames,'json_file_sha256':hashlib.sha256((ROOT/'visual-plan.json').read_bytes()).hexdigest(),'limitations':['No finished video or full-motion playback','No recorded VO or caption synchronization','No independent audience or subject-matter review','No platform overlay or phone-device testing','Not an all-object collision check','Contrast calculated for declared fully opaque text/background pairs, not animated composited states']}
(ROOT/'qa-results.json').write_text(json.dumps(result,indent=2)+'\n')
print('QA sheet and results generated; no image/video input used.')
