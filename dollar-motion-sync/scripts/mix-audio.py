#!/usr/bin/env python3
"""Original 120 BPM procedural bed, cue-driven SFX, and VO-driven music ducking."""
import csv,json,math,wave
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parents[1];A=P/'public/audio';plan=json.loads((P/'src/timeline.json').read_text());R=48000;N=15*R;t=np.arange(N)/R

def put(dst,start,s):
 n=min(len(s),len(dst)-start)
 if n>0:dst[start:start+n]+=s[:n]
def save(name,data):
 a=np.asarray(data);ch=1 if a.ndim==1 else a.shape[1]
 with wave.open(str(A/name),'wb') as w:w.setnchannels(ch);w.setsampwidth(2);w.setframerate(R);w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
def read_voice(path):
 with wave.open(str(path)) as w:a=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float64)/32768;sr=w.getframerate()
 return np.interp(np.arange(round(len(a)*R/sr))/R,np.arange(len(a))/sr,a)
def smoothed(values,attack_ms,release_ms):
 # input values at 10ms intervals, with attack/release exponential smoothing
 out=np.empty_like(values);v=0.
 for i,x in enumerate(values):
  tau=attack_ms if x>v else release_ms;c=math.exp(-10/tau);v=c*v+(1-c)*x;out[i]=v
 return out
# VO master, with moderate envelope compression; no claim of microphone or de-essing.
voice=np.zeros(N)
for i,s in enumerate(plan['scenes']):put(voice,round(s['voice_start']/30*R),read_voice(A/f'voice-{i+1}.wav'))
block=R//100; times=np.arange(N//block)*.01
rms=np.sqrt(np.mean(voice.reshape(-1,block)**2,axis=1));env=smoothed(rms,20,130)
threshold=.11;gain=np.minimum(1,(np.maximum(env,threshold)/threshold)**(1/2.2-1));voice*=np.interp(t,times,gain)*1.15
# Arrangement: original minor-key arpeggio, sub-bass, kick, snare, hats and pad.
rng=np.random.default_rng(716);music=np.zeros(N);beat=.5
notes=[146.83,174.61,220,196,164.81,196,246.94,220];bass=[55,55,65.41,49]
for i in range(60):
 at=i*beat/2;start=round(at*R);length=min(round(.30*R),N-start);x=np.arange(length)/R
 arpenv=(1-np.exp(-x*100))*np.exp(-x*9);hz=notes[i%len(notes)]
 put(music,start,.011*arpenv*(np.sin(2*np.pi*hz*x)+.25*np.sin(2*np.pi*hz*2*x)))
 hat=rng.normal(0,1,length);hat=np.concatenate(([0],np.diff(hat)));put(music,start,.003*hat*np.exp(-x*70))
 if i%2==0:
  k=.042*np.sin(2*np.pi*(90*x-110*x*x))*np.exp(-x*25);put(music,start,k)
  b=bass[(i//8)%4];benv=(1-np.exp(-x*80))*np.exp(-x*4.0);put(music,start,.024*benv*(np.sin(2*np.pi*b*x)+.2*np.sin(4*np.pi*b*x)))
 if i%4==2:
  snare=rng.normal(0,1,length);put(music,start,.009*snare*np.exp(-x*38))
music+=(.009*np.sin(2*np.pi*73.42*t)+.006*np.sin(2*np.pi*110*t))*(.75+.25*np.sin(2*np.pi*.1*t))
# Dynamic breakdown after the third narration and before payoff, then return on beat.
structure=np.ones(N);structure*=np.interp(t,[0,.12,9.95,10.25,10.7,11,14.35,15],[.2,1,1,.25,.25,1,1,0]);music*=structure
# VO-driven sidechain on music only; 10ms detector, 35ms attack / 240ms release.
detector=np.clip((rms-.004)/.025,0,1);duck=smoothed(detector,35,240);gain_db=-7.5*duck;music_ducked=music*np.interp(t,times,10**(gain_db/20))
sfx=np.zeros(N)
for c in plan['sound_cues']:
 frame=c['frame'];start=round(frame/30*R)
 if c['type']=='impact':
  n=min(round(.38*R),N-start);x=np.arange(n)/R
  impact=.075*np.sin(2*np.pi*(72*x-45*x*x))*np.exp(-x*15)+.035*rng.normal(0,1,n)*np.exp(-x*55)
  put(sfx,start,impact)
  if frame>10:
   dur=round(.16*R);u=np.arange(dur)/R;noise=rng.normal(0,1,dur);noise=np.concatenate(([0],np.diff(noise)));sweep=.011*noise*(u/.16)**2
   put(sfx,max(0,start-dur),sweep)
 else:
  n=min(round(.12*R),N-start);x=np.arange(n)/R;put(sfx,start,.022*np.sin(2*np.pi*(970*x+1400*x*x))*np.exp(-x*30))
mix=np.stack([voice+music_ducked+sfx,voice+music_ducked*.96+sfx*.92],axis=1);peak=float(np.max(np.abs(mix)))
if peak>.93:raise RuntimeError(f'Unacceptable pre-encode sample peak {peak}')
save('voice-processed.wav',voice);save('music-unducked.wav',music);save('music-ducked.wav',music_ducked);save('sfx.wav',sfx);save('mix.wav',mix)
with (P/'qa/ducking-curve.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['time_seconds','vo_rms','music_gain_db']);w.writerows(zip(times,np.round(rms,6),np.round(gain_db,4)))
report={'sample_rate':R,'duration_seconds':15,'voice':'Kokoro am_eric; RMS envelope compression threshold .11, ratio 2.2:1, detector 20ms attack / 130ms release, 1.15 makeup; no de-essing','music':'original procedural 120 BPM dark minor-key pulse; arranged reduction at 10.25-10.7 s then rises by 11s','sfx':'original procedural impact, noise risers and electronic ticks, placed by timeline cue frames','ducking':'music-only VO-driven 10ms RMS detector, 35ms attack/240ms release, 0 to -7.5 dB gain','minimum_music_gain_db':float(np.min(gain_db)),'maximum_music_gain_db':float(np.max(gain_db)),'pre_encode_sample_peak':peak,'pre_encode_rms':float(np.sqrt(np.mean(mix**2))),'note':'Measured gain values are applied control values, not subjective mix quality or true-peak/loudness certification. Human listening not performed.'}
(P/'audio-metadata.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
