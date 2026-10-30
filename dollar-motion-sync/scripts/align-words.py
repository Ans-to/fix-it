#!/usr/bin/env python3
"""Estimate word timing from the actual voice clips using a local faster-whisper model.
Automatic estimates are not human-verified word or syllable boundaries.
"""
import json, os, re, hashlib
from pathlib import Path
from faster_whisper import WhisperModel
P=Path(__file__).resolve().parents[1];voice=P/'public/audio'; meta=json.loads((voice/'voice-metadata.json').read_text())
modeldir=Path(os.environ.get('WHISPER_MODEL','/tmp/whisper-model'))
sha=hashlib.sha256((modeldir/'model.bin').read_bytes()).hexdigest()
model=WhisperModel(str(modeldir),device='cpu',compute_type='int8',cpu_threads=4)
starts=[3,105,210,330]; fps=30;clips=[]
normalize=lambda s:re.sub(r'[^a-z0-9\']','',s.lower())
for i,clip in enumerate(meta['clips']):
 segments,_=model.transcribe(str(voice/clip['file']),language='en',beam_size=5,word_timestamps=True,initial_prompt=clip['text'],vad_filter=False,condition_on_previous_text=False)
 words=[w for s in segments for w in s.words]
 expected=clip['text'].split()
 if [normalize(w.word) for w in words]!=[normalize(w) for w in expected]:
  raise ValueError(f"Transcript mismatch on clip {i+1}: {[w.word for w in words]} versus {expected}")
 timed=[]
 for expected_word,w in zip(expected,words):
  at=starts[i]/fps+float(w.start);end=starts[i]/fps+float(w.end)
  timed.append({'text':expected_word,'clip_start_seconds':float(w.start),'clip_end_seconds':float(w.end),'absolute_start_seconds':round(at,4),'absolute_end_seconds':round(end,4),'start_frame':round(at*fps),'end_frame':round(end*fps),'probability':round(float(w.probability),4)})
 clips.append({'id':i+1,'start_frame':starts[i],'text':clip['text'],'words':timed})
result={'method':'faster-whisper small CTranslate2 int8 word timestamps, run on each actual Kokoro clip; automatic estimates, not manually verified','model_sha256':sha,'fps':fps,'frame_rounding':'nearest frame, Python round','limitation':'Word starts and ends are estimates; neither phoneme/syllable alignment nor perceived sync was manually verified.','clips':clips}
(P/'src/word-cues.json').write_text(json.dumps(result,indent=2)+'\n')
print('Estimated',sum(len(c['words']) for c in clips),'words; normalized transcripts match.')
