#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent
voice=json.loads((p/'voice-metadata.json').read_text())
fontfiles=['fonts/Anton-Regular.ttf','fonts/Manrope-Variable.ttf','fonts/IBMPlexMono-Regular.ttf']
scenes=[
 {'id':'question','start':0,'end':85,'number':'01','eyebrow':'THE GLOBAL MONEY QUESTION','headline':['WHY THE','DOLLAR?'],'clip':1,'voice_start':5,'caption':['Why does so much of the world','rely on dollars?']},
 {'id':'markets','start':85,'end':195,'number':'02','eyebrow':'THE FINANCIAL FOUNDATION','headline':['DEEP MARKETS.','EASY TO TRADE.'],'clip':2,'voice_start':87,'caption':['Deep U.S. financial markets make','dollars easy to trade and hold.']},
 {'id':'network','start':195,'end':302,'number':'03','eyebrow':'THE NETWORK EFFECT','headline':['MORE USERS.','MORE USEFUL.'],'clip':3,'voice_start':197,'caption':['As more people accept dollars,','they become more useful to others.']},
 {'id':'payoff','start':302,'end':450,'number':'04','eyebrow':'THE SHORT ANSWER','headline':['THE LEADER.','NOT THE ONLY.'],'clip':4,'voice_start':303,'caption':["That helps the dollar lead, but it's",'not the only global currency.']},
]
for s in scenes:
 d=voice['clips'][s['clip']-1]['duration_seconds']
 s['voice_duration_seconds']=d;s['caption_start']=s['voice_start'];s['caption_end']=min(s['end'], s['voice_start']+int(d*30+0.999))
plan={
 'schema_version':'dollar-pillow-profile-1.0.0','purpose':'illustrative test, not approved production master',
 'format':{'width':1080,'height':1920,'fps':30,'fps_status':'PROPOSED','duration_seconds':15,'duration_status':'CONFIRMED','total_frames':450,'aspect_status':'PROPOSED','rationale':'Vertical test for Shorts, Reels and TikTok; exact dimensions/fps were not specified by user.'},
 'visual_authority':'This manifest controls scene timing, text, colors and fonts; render_video.py defines the dollar-pillow-profile-1.0.0 scene geometry and animation algorithms. audio_mix.py defines audio synthesis and uses voice_start positions here.',
 'coordinate_system':'Top-left; +x right, +y down; 1080x1920; text anchors as specified in renderer; screen-fixed elements.',
 'colors':{'paper':'#F4F1E9','ink':'#142738','blue':'#244BC7','muted':'#53616A','gold':'#C89045','cream':'#FDFCF8','white':'#FFFFFF','line':'#D9D9D1','navy':'#132939'},
 'assets':{'mode':'original procedural graphics; no image/video inputs','fonts':[{'path':f,'sha256':hashlib.sha256((p/f).read_bytes()).hexdigest()} for f in fontfiles]},
 'voice':{'engine':voice['engine'],'voice':voice['voice'],'model_sha256':voice['model_sha256'],'voice_sha256':voice['voice_sha256'],'speed':voice['speed'],'captions':'full sentence per clip, cue timings from measured clip duration; no word-level alignment claim'},
 'audio':{'sample_rate':48000,'channels':2,'music':'original procedural synthesized ambient bed','effects':'original procedural soft clicks and sweeps','end_fade_seconds':0.7},
 'scenes':scenes,
 'sources':['https://www.federalreserve.gov/econres/notes/feds-notes/2nd-annual-international-roles-of-the-us-dollar-conference-20230623.html','https://www.federalreserve.gov/econres/notes/feds-notes/fifth-conference-on-the-international-roles-of-the-u-s-dollar-stablecoins-digital-payments-and-the-ir-of-the-usd-20260716.html','https://www.federalreserve.gov/econres/notes/feds-notes/the-international-role-of-the-u-s-dollar-2025-edition-20250718.html']
}
(p/'visual-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
print('Plan written; actual source font hashes recorded.')
