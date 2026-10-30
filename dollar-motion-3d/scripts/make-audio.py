#!/usr/bin/env python3
"""Procedural music/effects aligned to the frame-driven edit; no sampled music."""
import json,wave
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parents[1];plan=json.loads((P/'src/plan.json').read_text());R=48000;dur=15;n=R*dur;t=np.arange(n)/R
# Original minor-key synth bed, evolving pulse and soft percussion.
track=np.zeros(n);beats=60/106
notes=[146.83,174.61,220,196,146.83,174.61,220,261.63]
for i,at in enumerate(np.arange(0,dur,beats/2)):
 start=int(at*R);length=min(int(.48*R),n-start);x=np.arange(length)/R
 env=np.exp(-x*7)*(1-np.exp(-x*80));hz=notes[i%len(notes)]
 track[start:start+length]+=.015*env*(np.sin(2*np.pi*hz*x)+.35*np.sin(2*np.pi*hz*2*x))
 if i%2==0:
  kick=.025*np.sin(2*np.pi*(90*x-35*np.minimum(x,.18)**2))*np.exp(-x*22)
  track[start:start+length]+=kick
pad=(.009*np.sin(2*np.pi*73.42*t)+.006*np.sin(2*np.pi*110*t)+.003*np.sin(2*np.pi*146.83*t))*(.7+.3*np.sin(2*np.pi*.09*t))
track+=pad
rng=np.random.default_rng(407)
for at in [0,85/30,195/30,302/30,270/30]:
 start=int(at*R);length=min(int(.4*R),n-start);x=np.arange(length)/R
 noise=np.convolve(rng.normal(0,1,length),np.ones(20)/20,mode='same')
 env=np.sin(np.pi*np.minimum(x/.4,1))**2
 fx=.035*noise*env + .035*np.sin(2*np.pi*(410*x+430*x*x))*np.exp(-x*19)
 track[start:start+length]+=fx
voice=np.zeros(n)
for s in plan['scenes']:
 with wave.open(str(P/f"public/audio/voice-{plan['scenes'].index(s)+1}.wav"),'rb') as w:
  a=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768;source=w.getframerate()
 a=np.interp(np.arange(round(len(a)*R/source))/R,np.arange(len(a))/source,a)
 start=round(s['voice_start']/30*R);voice[start:start+len(a)]+=a
fade=np.minimum(1,t/.25)*np.minimum(1,(dur-t)/.65)
track*=fade;mix=np.stack([voice*.96+track,voice*.96+track*.94],axis=1)
peak=float(np.max(np.abs(mix)));rms=float(np.sqrt(np.mean(mix*mix)))
if peak>.95:raise ValueError('mix exceeds headroom')
with wave.open(str(P/'public/audio/audio-mix.wav'),'wb') as w:
 w.setnchannels(2);w.setsampwidth(2);w.setframerate(R);w.writeframes((mix*32767).astype('<i2').tobytes())
(P/'audio-metadata.json').write_text(json.dumps({'duration_seconds':15,'sample_rate':R,'voice':'am_eric, unchanged clips from prior test','music':'original procedural minor-key pulse, 106 BPM','sfx':'original procedural transition swooshes and short impacts','peak_linear':peak,'rms_linear':rms,'limitations':'generated signal has not received a human listening review'},indent=2)+'\n')
print('Wrote soundtrack, peak',peak,'RMS',rms)
