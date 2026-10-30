#!/usr/bin/env python3
"""Report frame quantization against automatic timestamps, not acoustic truth."""
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1];plan=json.loads((P/'src/timeline.json').read_text());a=json.loads((P/'src/word-cues.json').read_text());fps=plan['format']['fps'];titles={x['id']:x for x in plan['titles']};fx={x['id']:x for x in plan['sound_cues']}
items=[]
for title,clip,index,sfx in [('world',1,3,None),('dollar',1,5,'dollar-hit'),('america',1,7,None),('trade',2,6,'trade-tick'),('connections',3,6,'new-node'),('only',4,5,'qualifier')]:
 w=a['clips'][clip-1]['words'][index];f=titles[title]['start'];items.append({'title_id':title,'word':w['text'],'automatic_onset_seconds':w['absolute_start_seconds'],'visual_frame':f,'visual_minus_estimate_ms':round((f/fps-w['absolute_start_seconds'])*1000,3),'sfx_id':sfx,'sfx_frame':fx[sfx]['frame'] if sfx else None,'visual_sfx_frame_offset':fx[sfx]['frame']-f if sfx else None})
report={'fps':fps,'type':'timeline consistency against automatic ASR estimates; not proof of audible sync','events':items,'scene_beat_frames':[105,210,330],'beat_spacing_frames':fps*60/plan['beats_per_minute'],'limits':'ASR errors, AAC encoding, signal latency, acoustic onset, phoneme alignment, perceived timing and listening are not evaluated.'}
(P/'qa/sync-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
