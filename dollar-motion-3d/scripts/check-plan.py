#!/usr/bin/env python3
"""Structural and timing checks; not a rendered-video quality or accessibility test."""
from pathlib import Path
import json,unittest,wave,hashlib
from jsonschema import Draft202012Validator
P=Path(__file__).resolve().parents[1]
class PlanTests(unittest.TestCase):
 def setUp(self):
  self.plan=json.loads((P/'src/plan.json').read_text());self.meta=json.loads((P/'voice-metadata.json').read_text())
 def test_schema(self):
  schema=json.loads((P/'manifest.schema.json').read_text());Draft202012Validator.check_schema(schema);Draft202012Validator(schema).validate(self.plan)
 def test_timeline(self):
  p=self.plan;f=p['format'];self.assertEqual(f['fps']*f['duration_seconds'],f['duration_frames']);self.assertEqual(p['scenes'][0]['start'],0);self.assertEqual(p['scenes'][-1]['end'],f['duration_frames'])
  for i,s in enumerate(p['scenes']):
   self.assertLess(s['start'],s['end']);self.assertGreaterEqual(s['voice_start'],s['start']);self.assertLessEqual(s['voice_start']+s['voice_duration']*f['fps'],s['end'])
   if i:self.assertEqual(p['scenes'][i-1]['end'],s['start'])
 def test_audio_and_captions_match_metadata(self):
  self.assertEqual(len(self.plan['scenes']),len(self.meta['clips']))
  for i,(s,v) in enumerate(zip(self.plan['scenes'],self.meta['clips']),1):
   self.assertEqual(' '.join(s['caption']),v['text']);self.assertAlmostEqual(s['voice_duration'],v['duration_seconds'],places=5)
   with wave.open(str(P/'public/audio'/f'voice-{i}.wav')) as w:self.assertAlmostEqual(w.getnframes()/w.getframerate(),v['duration_seconds'],places=4)
  with wave.open(str(P/'public/audio/audio-mix.wav')) as w:self.assertEqual((w.getnchannels(),w.getframerate(),w.getnframes()),(2,48000,15*48000))
 def test_assets_and_srt(self):
  for name in ['Anton-Regular.ttf','Manrope-Variable.ttf','IBMPlexMono-Regular.ttf']:
   self.assertGreater((P/'public/fonts'/name).stat().st_size,10000)
  srt=(P/'captions.srt').read_text();self.assertEqual(srt.count(' --> '),4)
  for s in self.plan['scenes']:self.assertIn('\n'.join(s['caption']),srt)
if __name__=='__main__':unittest.main(verbosity=2)
