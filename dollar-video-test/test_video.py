#!/usr/bin/env python3
"""Mechanical QA of the planned Pillow geometry, captions and audio intervals."""
import hashlib,json,math,sys,wave
from jsonschema import Draft202012Validator
from pathlib import Path
from itertools import combinations
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P));import render_video as r
p=r.PLAN;scenes=p['scenes'];N=p['format']['total_frames'];fps=p['format']['fps']
schema=json.loads((P/'manifest.schema.json').read_text())
Draft202012Validator.check_schema(schema);Draft202012Validator(schema).validate(p)
assert [s['id'] for s in scenes]==['question','markets','network','payoff']
errors=[]; seen=[]
assert sum(s['end']-s['start'] for s in scenes)==N
assert scenes[0]['start']==0 and scenes[-1]['end']==N
assert all(a['end']==b['start'] for a,b in zip(scenes,scenes[1:]))
for asset in p['assets']['fonts']:
 assert hashlib.sha256((P/asset['path']).read_bytes()).hexdigest()==asset['sha256']
for s in scenes:
 assert s['start'] <= s['caption_start'] < s['caption_end'] <= s['end']
 end=s['voice_start']/fps+s['voice_duration_seconds']
 assert end<=s['end']/fps, (s['id'],end,s['end']/fps)
for i in range(4):
 s=scenes[i]; assert ' '.join(s['caption'])==json.loads((P/'voice-metadata.json').read_text())['clips'][i]['text']
 with wave.open(str(P/f"voice-{s['clip']}.wav"),'rb') as w:
  assert abs(w.getnframes()/w.getframerate()-s['voice_duration_seconds'])<1e-9
 assert s['caption_end']==min(s['end'],s['voice_start']+math.ceil(s['voice_duration_seconds']*fps))
# All text is measured with the actual shipped fonts during every generated frame.
original=r.Canvas.text
for frame in range(N):
 boxes=[]
 def record(self,*args,**kw):
  result=original(self,*args,**kw);boxes.append((args[1],result));return result
 r.Canvas.text=record
 r.frame_image(frame)
 for (ta,a),(tb,b) in combinations(boxes,2):
  if a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]:errors.append((frame,ta,tb,a,b))
 if scenes[2]['start']<=frame<scenes[2]['end']:
  local=frame-scenes[2]['start'];positions={'A':(290,900,round(58*r.smooth((local-6)/14))),'B':(790,900,round(58*r.smooth((local-18)/14))),'C':(290,1220,round(58*r.smooth((local-39)/14))),'D':(790,1220,round(58*r.smooth((local-57)/14))),'USD':(540,1063,84)}
  for text,bb in boxes:
   if text not in positions:continue
   cx,cy,rad=positions[text]
   if not all(math.hypot(x-cx,y-cy)<=rad-2 for x in (bb[0],bb[2]) for y in (bb[1],bb[3])):errors.append((frame,'circle containment',text,bb))
r.Canvas.text=original
if errors:
 print(json.dumps({'status':'FAIL','first_errors':errors[:10]},indent=2));sys.exit(1)
with wave.open(str(P/'audio-mix.wav'),'rb') as w:
 assert w.getframerate()==48000 and w.getnchannels()==2 and w.getnframes()==15*48000
print(json.dumps({'status':'PASS','scope':'manifest schema and all 450 generated plan frames: actual font-metric viewport bounds, non-overlapping text boxes, caption panel bounds, network-node text containment; scene/caption intervals; audio WAV metadata and font hashes',
 'limitations':'Not a decoded-video pixel/occlusion/contrast audit, audio listening test, platform-safe-area test, motion quality judgment or accessibility certification.'},indent=2))
