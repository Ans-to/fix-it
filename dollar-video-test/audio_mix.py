#!/usr/bin/env python3
"""Original procedural bed and effects, mixed with four Kokoro speech clips."""
import json,math,wave
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
plan=json.loads((P/'visual-plan.json').read_text())
SR=48000; dur=15; n=SR*dur;t=np.arange(n,dtype=np.float64)/SR
# Warm, restrained tonal bed, generated from scratch and ducked relative to speech.
bed=np.zeros(n,dtype=np.float64)
for hz,amp in [(130.81,.007),(196.0,.004),(261.63,.003)]:
 bed+=amp*np.sin(2*np.pi*hz*t + .08*np.sin(2*np.pi*.09*t))
# A very soft pulsing overtone; no sampled music or effects.
bed+=.0035*np.sin(2*np.pi*392*t)*(.5+.5*np.cos(2*np.pi*.55*t))
bed*=np.minimum(1,t/.5)*np.minimum(1,(dur-t)/.7)
mix=np.stack([bed,bed],axis=1);voice_track=np.zeros(n,dtype=np.float64)
for scene in plan['scenes']:
 with wave.open(str(P/f"voice-{scene['clip']}.wav"),'rb') as w:
  a=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float64)/32768
  source_sr=w.getframerate()
 resampled=np.interp(np.arange(round(len(a)*SR/source_sr))/SR,np.arange(len(a))/source_sr,a)
 start=round(scene['voice_start']/plan['format']['fps']*SR);end=start+len(resampled)
 if end>n:raise ValueError('voice exceeds video')
 voice_track[start:end]+=resampled
mix+=voice_track[:,None]*.96
# Original synthesized, short, subdued transient and sweep on scene starts.
rng=np.random.default_rng(1045)
for scene in plan['scenes']:
 start=round(scene['start']/plan['format']['fps']*SR)
 length=min(round(.22*SR),n-start);s=np.arange(length)/SR
 noise=rng.normal(0,1,length)
 # Smooth the noise so it does not become an overly sharp hiss.
 kernel=np.ones(31)/31;noise=np.convolve(noise,kernel,mode='same')
 env=np.sin(np.pi*np.minimum(s/.22,1))**2
 sw=.018*noise*env + .024*np.sin(2*np.pi*(340*s+350*s*s))*np.exp(-s*21)
 mix[start:start+length,0]+=sw;mix[start:start+length,1]+=sw*.88
fade=np.minimum(1,(dur-t)/.08);mix*=fade[:,None]
peak=float(np.max(np.abs(mix)));rms=float(np.sqrt(np.mean(mix**2)))
if peak>.95:raise ValueError(f'unexpected mix peak {peak}')
def write(path,data):
 pcm=(np.clip(data,-1,1)*32767).astype('<i2')
 with wave.open(str(path),'wb') as w:
  w.setnchannels(1 if pcm.ndim==1 else pcm.shape[1]);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
write(P/'audio-mix.wav',mix);write(P/'voiceover.wav',voice_track)
(P/'audio-metadata.json').write_text(json.dumps({'sample_rate':SR,'channels':2,'duration_seconds':dur,'peak_linear':peak,'rms_linear':rms,'source':'original procedural music/effects plus Kokoro am_eric; no sampled music','review':'Numerical signal checks only; human listening not performed.'},indent=2)+'\n')
print(f'audio generated: peak={peak:.4f}, RMS={rms:.4f}, duration={dur}s')
