#!/usr/bin/env python3
"""Checks declared structure/cues, not audible or perceived sync."""
import csv,json,math,re,unittest,wave
from pathlib import Path
from jsonschema import Draft202012Validator
P=Path(__file__).resolve().parents[1];plan=json.loads((P/'src/timeline.json').read_text());alignment=json.loads((P/'src/word-cues.json').read_text());meta=json.loads((P/'public/audio/voice-metadata.json').read_text());scenes=plan['scenes'];fps=plan['format']['fps']
class Plan(unittest.TestCase):
 def test_schema_and_dimensions(self):
  schema=json.loads((P/'manifest.schema.json').read_text());Draft202012Validator.check_schema(schema);Draft202012Validator(schema).validate(plan)
  self.assertEqual((plan['format']['width'],plan['format']['height'],fps,plan['format']['duration_frames']),(1080,1920,30,450))
 def test_coverage_and_audio(self):
  self.assertEqual(len(scenes),len(alignment['clips']));self.assertEqual(len(scenes),len(meta['clips']))
  self.assertEqual(scenes[0]['start'],0);self.assertEqual(scenes[-1]['end'],450)
  for i,s in enumerate(scenes):
   if i:self.assertEqual(scenes[i-1]['end'],s['start'])
   self.assertLess(s['start'],s['end']);self.assertEqual(s['voice_start'],alignment['clips'][i]['start_frame'])
   self.assertLessEqual(s['voice_start']+s['voice_duration']*fps,s['end'])
   self.assertEqual(' '.join(w for line in s['caption_lines'] for w in line),meta['clips'][i]['text'])
   self.assertEqual([w for line in s['caption_lines'] for w in line],[w['text'] for w in alignment['clips'][i]['words']])
   with wave.open(str(P/'public/audio'/f'voice-{i+1}.wav')) as w:self.assertAlmostEqual(w.getnframes()/w.getframerate(),s['voice_duration'],places=5)
  with wave.open(str(P/'public/audio/mix.wav')) as w:self.assertEqual((w.getnchannels(),w.getframerate(),w.getnframes()),(2,48000,720000))
 def test_cues_quantization_and_titles(self):
  for c in alignment['clips']:
   for w in c['words']:
    self.assertLessEqual(abs(w['start_frame']/fps-w['absolute_start_seconds']),1/(2*fps)+.0001)
    self.assertLessEqual(w['start_frame'],w['end_frame'])
  titles=plan['titles'];self.assertEqual(titles[0]['start'],0);self.assertEqual(titles[-1]['end'],450)
  for i,x in enumerate(titles):
   self.assertLess(x['start'],x['end'])
   if i:self.assertEqual(titles[i-1]['end'],x['start'])
  lookup=lambda i,j:alignment['clips'][i-1]['words'][j]['start_frame']
  starts={t['id']:t['start'] for t in titles};effects={c['id']:c['frame'] for c in plan['sound_cues']}
  for a,b in [('world',lookup(1,3)),('dollar',lookup(1,5)),('america',lookup(1,7)),('trade',lookup(2,6)),('connections',lookup(3,6)),('only',lookup(4,5))]:self.assertEqual(starts[a],b)
  for a,b in [('dollar-hit',lookup(1,5)),('trade-tick',lookup(2,6)),('new-node',lookup(3,6)),('qualifier',lookup(4,5))]:self.assertEqual(effects[a],b)
 def test_beat_grid_and_duck_control(self):
  beat_frames=fps*60/plan['beats_per_minute'];self.assertEqual(beat_frames,15)
  for s in scenes[1:]:self.assertEqual((s['start']-plan['beat_origin_frame'])%beat_frames,0)
  with (P/'qa/ducking-curve.csv').open() as f: rows=list(csv.DictReader(f))
  g=[float(r['music_gain_db']) for r in rows];self.assertEqual(len(g),1500);self.assertLessEqual(min(g),-7.4);self.assertAlmostEqual(max(g),0);self.assertGreaterEqual(min(g),-7.501)
 def test_caption_and_font_presence(self):
  text=(P/'captions.srt').read_text();self.assertEqual(text.count(' --> '),4)
  for s in scenes:self.assertIn('\n'.join(' '.join(line) for line in s['caption_lines']),text)
  for x in ('Anton-Regular.ttf','Manrope-Variable.ttf','IBMPlexMono-Regular.ttf'):self.assertGreater((P/'public/fonts'/x).stat().st_size,10000)
if __name__=='__main__':unittest.main(verbosity=2)
