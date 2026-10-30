#!/usr/bin/env python3
"""Build phrase-level SRT from clip starts and lengths in the timeline."""
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1];plan=json.loads((P/'src/timeline.json').read_text());fps=plan['format']['fps']
def t(x):
 ms=round(x*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
with (P/'captions.srt').open('w') as f:
 for i,s in enumerate(plan['scenes'],1):
  start=s['voice_start']/fps;end=start+s['voice_duration'];f.write(f"{i}\n{t(start)} --> {t(end)}\n"+'\n'.join(' '.join(line) for line in s['caption_lines'])+'\n\n')

p=P/'captions.srt';p.write_text(p.read_text().rstrip()+'\n')
