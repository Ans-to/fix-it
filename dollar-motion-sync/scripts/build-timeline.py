#!/usr/bin/env python3
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1];cues=json.loads((P/'src/word-cues.json').read_text());clips=cues['clips']
def word(n,i):return clips[n-1]['words'][i]['start_frame']
beats=[{'id':'hook','start':0,'end':105,'voice_start':3,'voice_duration':2.8097916666666665,'caption_lines':[['Why','does','the','world','use'],['dollars?',"It's",'not','just','America.']]},
 {'id':'markets','start':105,'end':210,'voice_start':105,'voice_duration':2.7705416666666665,'caption_lines':[['Deep','markets','make','dollars','easier'],['to','trade','and','hold.']]},
 {'id':'network','start':210,'end':330,'voice_start':210,'voice_duration':3.165791666666667,'caption_lines':[['As','more','people','accept','them,'],['more','connections','become','possible.']]},
 {'id':'qualifier','start':330,'end':450,'voice_start':330,'voice_duration':2.8752916666666666,'caption_lines':[['The','dollar','leads.'],['But',"it's",'not','the','only','global','currency.']]}]
titles=[
 {'id':'why','start':0,'end':word(1,3),'lines':['WHY?'],'cue':'clip 1 word 1 (shown immediately for the hook)','style':'burst'},
 {'id':'world','start':word(1,3),'end':word(1,5),'lines':['THE WORLD'],'cue':'clip 1 world','style':'left'},
 {'id':'dollar','start':word(1,5),'end':word(1,7),'lines':['DOLLARS?'],'cue':'clip 1 dollars','style':'burst'},
 {'id':'america','start':word(1,7),'end':105,'lines':['NOT JUST','AMERICA.'],'cue':'clip 1 not','style':'right'},
 {'id':'markets','start':105,'end':word(2,6),'lines':['DEEP','MARKETS.'],'cue':'clip 2 deep','style':'left'},
 {'id':'trade','start':word(2,6),'end':210,'lines':['TRADE','& HOLD.'],'cue':'clip 2 trade','style':'right'},
 {'id':'people','start':210,'end':word(3,6),'lines':['MORE','PEOPLE.'],'cue':'clip 3 as','style':'left'},
 {'id':'connections','start':word(3,6),'end':330,'lines':['MORE','CONNECTIONS.'],'cue':'clip 3 connections','style':'right'},
 {'id':'leads','start':330,'end':word(4,5),'lines':['THE DOLLAR','LEADS.'],'cue':'clip 4 the','style':'left'},
 {'id':'only','start':word(4,5),'end':450,'lines':['NOT THE','ONLY ONE.'],'cue':'clip 4 not','style':'right'}]
effects=[{'id':'opening-impact','frame':0,'type':'impact','reason':'intro'},
 {'id':'dollar-hit','frame':word(1,5),'type':'impact','reason':'dollars emphasized'},
 {'id':'markets-downbeat','frame':105,'type':'impact','reason':'markets on 120 BPM beat'},
 {'id':'trade-tick','frame':word(2,6),'type':'tick','reason':'trade word'},
 {'id':'network-downbeat','frame':210,'type':'impact','reason':'network on 120 BPM beat'},
 {'id':'new-node','frame':word(3,6),'type':'tick','reason':'connections word'},
 {'id':'payoff-downbeat','frame':330,'type':'impact','reason':'payoff on 120 BPM beat'},
 {'id':'qualifier','frame':word(4,5),'type':'tick','reason':'not emphasized'}]
plan={'schema_version':'motion-sync-v1.0.0','status':'ILLUSTRATIVE TEST — output geometry and timing proposed','format':{'width':1080,'height':1920,'fps':30,'duration_frames':450},'voice':'Kokoro-82M-v1.0 q8 am_eric speed 1.08','beats_per_minute':120,'beat_origin_frame':0,'scenes':beats,'titles':titles,'sound_cues':effects,'sources':['https://www.federalreserve.gov/econres/notes/feds-notes/2nd-annual-international-roles-of-the-us-dollar-conference-20230623.html','https://www.federalreserve.gov/econres/notes/feds-notes/fifth-conference-on-the-international-roles-of-the-u-s-dollar-stablecoins-digital-payments-and-the-ir-of-the-usd-20260716.html','https://www.federalreserve.gov/econres/notes/feds-notes/the-international-role-of-the-u-s-dollar-2025-edition-20250718.html']}
(P/'src/timeline.json').write_text(json.dumps(plan,indent=2)+'\n')
for s in beats: print(s['id'],s['start'],s['voice_start'],round(s['voice_duration'],2))
for e in titles: print(e['id'],e['start'],e['end'])
