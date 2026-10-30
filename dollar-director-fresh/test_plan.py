#!/usr/bin/env python3
"""Inspect storyboard state; no video, photograph or image assets are used as input.
Requires Pillow. This is limited mechanical QA, not an audience or audio test.
"""
import json, math, re, hashlib
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
plan=json.loads((ROOT/'visual-plan.json').read_text()); F=plan['format']; palette=plan['palette']
W,H,FPS,N=(F[k] for k in ('width','height','fps','frame_count'))
@lru_cache(None)
def font(size):return ImageFont.truetype(plan['font']['path_for_reference_test'],size)
@lru_cache(None)
def relbox(t,size):return ImageDraw.Draw(Image.new('RGB',(1,1))).textbbox((0,0),t,font=font(size),anchor='mm')
def rgb(name):
 h=palette[name].lstrip('#');return tuple(int(h[i:i+2],16) for i in (0,2,4))
def smooth(t):
 u=max(0,min(1,t));return u*u*(3-2*u)
def intersect(a,b):return a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]
def find_scene(f):return next(s for s in plan['scenes'] if s['interval'][0]<=f<s['interval'][1])
def state(scene,f,o):
 local=f-scene['interval'][0]; d=o.get('delay',0 if o['group']=='screen' else 6); alpha=smooth((local-d)/18)
 if 'fade_out' in o:
  a,b=o['fade_out'];alpha*=1-smooth((local-a)/(b-a))
 duration=scene['interval'][1]-scene['interval'][0];z0,z1=scene['camera']['zoom'];z=1 if o['group']=='screen' else z0+(z1-z0)*smooth(local/(duration-1)); ax,ay=scene['camera']['zoom_anchor']
 def point(x,y):return (x,y) if o['group']=='screen' else (ax+(x-ax)*z,ay+(y-ay)*z)
 motion=o.get('x_motion');xx=None
 if motion:xx=motion['from']+(motion['to']-motion['from'])*smooth((local-motion['local_start'])/(motion['local_end']-motion['local_start']))
 return alpha,z,point,xx
def bounds(scene,f,o):
 alpha,z,point,xx=state(scene,f,o);kind=o['type']
 if kind=='text':
  x,y=o['center'];x,y=point(xx if xx is not None else x,y);b=relbox(o['value'],max(1,round(o['font_px']*z))); x,y=round(x),round(y);return (x+b[0],y+b[1],x+b[2],y+b[3])
 if kind=='circle':
  x,y=o['center'];x,y=point(xx if xx is not None else x,y);r=o['radius']*z;return (x-r,y-r,x+r,y+r)
 if kind=='rect':
  x,y=o['xy'];w,h=o['size'];x1,y1=point(x,y);x2,y2=point(x+w,y+h);return (x1,y1,x2,y2)
 x1,y1=point(*o['from']);x2,y2=point(*o['to']);return (min(x1,x2),min(y1,y2),max(x1,x2),max(y1,y2))
def draw_frame(f):
 s=find_scene(f);im=Image.new('RGBA',(W,H),rgb('night')+(255,))
 for o in sorted(s['objects'],key=lambda ob: 1 if ob['group']=='screen' else 0):
  a,z,point,xx=state(s,f,o)
  if a<=0:continue
  layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer);opacity=round(255*a)
  def col(c):return rgb(c)+(opacity,)
  if o['type']=='text':
   x,y=o['center'];x,y=point(xx if xx is not None else x,y)
   d.text((round(x),round(y)),o['value'],font=font(max(1,round(o['font_px']*z))),fill=col(o['color']),anchor='mm')
  elif o['type']=='circle':d.ellipse(bounds(s,f,o),fill=col(o['fill']),outline=col(o['stroke']),width=max(1,round(o['stroke_px']*z)))
  elif o['type']=='rect':d.rounded_rectangle(bounds(s,f,o),radius=round(o['radius']*z),fill=col(o['fill']),outline=col(o['stroke']),width=max(1,round(o['stroke_px']*z)))
  else:
   a1=point(*o['from']);a2=point(*o['to']);d.line((*a1,*a2),fill=col(o['color']),width=max(1,round(o['stroke_px']*z)))
  im=Image.alpha_composite(im,layer)
 cue=next(c for c in s['captions'] if c['interval'][0]<=f<c['interval'][1]);d=ImageDraw.Draw(im)
 d.rounded_rectangle((70,1510,1010,1690),radius=24,fill=rgb('surface')+(255,))
 ys=[1600] if len(cue['lines'])==1 else [1568,1635]
 for y,line in zip(ys,cue['lines']):d.text((540,y),line,font=font(42),fill=rgb('ivory')+(255,),anchor='mm')
 return im.convert('RGB')

def contrast(a,b):
 def luminance(c):
  def lin(x):
   x=x/255;return x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4
  return .2126*lin(c[0])+.7152*lin(c[1])+.0722*lin(c[2])
 a,b=sorted((luminance(rgb(a)),luminance(rgb(b))),reverse=True);return round((a+.05)/(b+.05),2)

assert (W,H,FPS,N)==(1080,1920,30,1800)
assert len(plan['scenes'])==8
cursor=0
for s in plan['scenes']:
 a,b=s['interval'];assert a==cursor and b>a;cursor=b
 assert s['camera']['viewport_center']==[540,960] and s['camera']['zoom_anchor']==[540,960]
 assert s['camera']['angle_degrees']=={'yaw':0,'pitch':0,'roll':0}
 assert len({o['id'] for o in s['objects']})==len(s['objects'])
 assert all(o['type'] in {'text','rect','circle','line'} for o in s['objects'])
 assert all(next(o for o in s['objects'] if o['id']==key)['group']=='screen' for key in ('heading','subheading'))
 assert s['captions'][0]['interval'][0]==a and s['captions'][-1]['interval'][1]==b
 assert all(x['interval'][1]==y['interval'][0] for x,y in zip(s['captions'],s['captions'][1:]))
 assert ' '.join(x for cap in s['captions'] for x in cap['lines'])==s['voiceover']
 assert all(1<=len(cap['lines'])<=2 for cap in s['captions'])
assert cursor==N
# Node endpoints remain attached in world space; all world objects share the same camera transform and no entry offset.
for sid in ('07_network','08_payoff'):
 scene=next(s for s in plan['scenes'] if s['id']==sid);obj={o['id']:o for o in scene['objects']};hub=obj['hub']
 links=[('left_link','left_node'),('right_link','right_node'),('bottom_link','bottom_node')] if sid=='07_network' else [('euro_link','euro_node'),('yen_link','yen_node'),('other_link','other_node')]
 for line_id,node_id in links:
  l,n=obj[line_id],obj[node_id]
  assert math.dist(l['from'],hub['center'])<=hub['radius']
  assert math.dist(l['to'],n['center'])<=n['radius']
# Label-to-container checks only for named pairs, not all shape interactions.
contain={
 '02_definition':[('trade','card_a'),('finance','card_b'),('reserves','card_c')],
 '03_history':[('year','history_card'),('history_label','history_card')],
 '04_gold_link':[('currency1','currencies_card'),('currency2','currencies_card'),('usd','usd_card'),('gold','gold_card')],
 '05_1971':[('dollar','dollar_panel'),('gold','gold_panel')],
 '06_reasons':[('economy','economy_card'),('treasury','treasury_card'),('invoicing','trade_card')],
}
issues=[];word_count=0;rates={}
for s in plan['scenes']:
 words=len(re.findall(r"[\w]+(?:['’][\w]+)?",s['voiceover']));word_count+=words;rate=words*60*FPS/(s['interval'][1]-s['interval'][0]);rates[s['id']]=round(rate,1)
for f in range(N):
 s=find_scene(f);objs={o['id']:o for o in s['objects']};previous=[]
 cue=[c for c in s['captions'] if c['interval'][0]<=f<c['interval'][1]]
 if len(cue)!=1:issues.append(f'{f}: caption coverage')
 else:
  ys=[1600] if len(cue[0]['lines'])==1 else [1568,1635]
  for y,line_text in zip(ys,cue[0]['lines']):
   b=relbox(line_text,42);b=(540+b[0],y+b[1],540+b[2],y+b[3])
   if b[0]<100 or b[2]>980 or b[1]<1510 or b[3]>1690:issues.append(f'{f}: caption outside box {b}')
 for name,container in contain.get(s['id'],[]):
  o,r=objs[name],objs[container]
  if state(s,f,o)[0]>0 and state(s,f,r)[0]>0:
   t,b=bounds(s,f,o),bounds(s,f,r)
   if t[0]<b[0]+8 or t[1]<b[1]+8 or t[2]>b[2]-8 or t[3]>b[3]-8:issues.append(f'{f}: {name} escapes {container}')
 for o in s['objects']:
  if state(s,f,o)[0]<=0:continue
  b=bounds(s,f,o)
  if b[0]<40 or b[2]>W-40 or b[1]<80 or b[3]>1450:issues.append(f'{f}: {o["id"]} out of composition {b}')
  if o['type']=='text':
   for other,otherbox in previous:
    if intersect(b,otherbox):issues.append(f'{f}: text overlap {other} and {o["id"]}')
   previous.append((o['id'],b))
ratios={f'{x}/{y}':contrast(x,y) for x,y in [('ivory','night'),('slate','night'),('gold','night'),('ivory','surface'),('gold','surface'),('night','gold')]}
assert min(ratios.values())>=4.5
print('Frame coverage:',cursor,'of',N,'; duration:',N/FPS,'seconds')
print('Selected layout checks:',N,'frames; issues:',len(issues))
print('Draft VO token count:',word_count,'; per-scene estimated token rates:',rates)
print('Fully opaque nominal color contrast:',ratios)
if issues:
 print('\n'.join(issues[:20]));raise SystemExit(1)
frames=[s['interval'][0]+(s['interval'][1]-s['interval'][0])//2 for s in plan['scenes']]
sheet=Image.new('RGB',(216*4,(384+28)*2),'white');d=ImageDraw.Draw(sheet)
for i,(s,f) in enumerate(zip(plan['scenes'],frames)):
 x=i%4*216;y=i//4*412;d.text((x+4,y+6),f'{s["id"]} / frame {f}',fill='black');sheet.paste(draw_frame(f).resize((216,384)),(x,y+28))
sheet.save(ROOT/'qa-contact-sheet.png')
(ROOT/'qa-results.json').write_text(json.dumps({'frames_checked':N,'duration_seconds':N/FPS,'selected_issues':0,'voiceover_estimated_tokens':word_count,'estimated_tokens_per_minute_by_scene':rates,'nominal_contrast_ratios':ratios,'preview_frames':frames,'manifest_sha256':hashlib.sha256((ROOT/'visual-plan.json').read_bytes()).hexdigest(),'limitations':['No actual video or audio rendered','Not a full all-object collision test','No audio sync test','No platform safe-area verification','No human comprehension or retention test','Contrast only fully opaque flat colors']},indent=2)+'\n')
print('QA contact sheet and results saved.')
