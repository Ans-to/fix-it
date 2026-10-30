import React, {useEffect, useMemo, useState} from 'react';
import {AbsoluteFill, continueRender, delayRender, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';
import {CyberAtmosphere} from '../components/CyberAtmosphere';
import {CinematicWord} from '../components/CinematicWord';
import {AudioTrack} from '../audio/AudioTrack';
import {SCENE_1_DURATION, SCENE_1_TIMINGS as t} from '../config/mockTimings';

// Only these four palette colors are used in the scene; opacity supplies hierarchy.
const VOID = '#050507';
const LIME = '#D2FF52';
const WHITE = '#FFFFFF';
const HUD = '#1E2229';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const lerp = (frame: number, input: number[], output: number[]) => interpolate(frame, input, output, clamp);

const makeDollarTexture = () => {
  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext('2d');
  if (!ctx) throw new Error('Unable to create the dollar texture.');
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = LIME;
  ctx.shadowColor = LIME;
  ctx.shadowBlur = 24;
  ctx.font = 'bold 310px Arial, sans-serif';
  ctx.fillText('$', 256, 270);
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  return texture;
};

/** Frame-driven 3D wireframe token. Basic materials avoid muddy lighting. */
const Dollar: React.FC<{frame: number}> = ({frame}) => {
  const texture = useMemo(makeDollarTexture, []);
  useEffect(() => () => texture.dispose(), [texture]);
  const travel = lerp(frame, [t.using, t.neither, 123], [0, 0.5, 1]);
  // Keep the moving token between the HUD terminals, never over their labels.
  const x = -0.18 + travel * 0.36;
  const y = Math.sin(travel * Math.PI) * 0.12;
  return <group position={[x, y, 0.35]} rotation={[0.08, 0.35 + frame * 0.036, 0]} scale={0.85}>
    <mesh><circleGeometry args={[0.43, 64]} /><meshBasicMaterial toneMapped={false} color={VOID} side={THREE.DoubleSide} /></mesh>
    {[-0.065, 0.065].map((z) => <group key={z} position={[0, 0, z]}>
      <mesh><torusGeometry args={[0.43, 0.009, 8, 64]} /><meshBasicMaterial toneMapped={false} color={LIME} /></mesh>
      <mesh><torusGeometry args={[0.36, 0.003, 6, 64]} /><meshBasicMaterial toneMapped={false} color={WHITE} transparent opacity={0.8} /></mesh>
      <mesh rotation={[0, z < 0 ? Math.PI : 0, 0]}><planeGeometry args={[0.58, 0.58]} /><meshBasicMaterial toneMapped={false} map={texture} transparent side={THREE.DoubleSide} /></mesh>
    </group>)}
    {Array.from({length: 16}, (_, i) => <mesh key={i} position={[0.43 * Math.cos(i * Math.PI / 8), 0.43 * Math.sin(i * Math.PI / 8), 0]}>
      <boxGeometry args={[0.008, 0.008, 0.13]} /><meshBasicMaterial toneMapped={false} color={LIME} />
    </mesh>)}
    <mesh rotation={[0.6, 0.4, frame * 0.018]}><torusGeometry args={[0.50, 0.003, 6, 80]} /><meshBasicMaterial toneMapped={false} color={WHITE} transparent opacity={0.65} /></mesh>
  </group>;
};

const CameraRig: React.FC<{frame: number; fps: number}> = ({frame, fps}) => {
  const {camera} = useThree();
  const push = spring({frame: frame - 8, fps, config: {mass: 0.4, stiffness: 115, damping: 18}});
  camera.position.set(Math.sin(frame * 0.025) * 0.08, Math.cos(frame * 0.018) * 0.04, 10.4 - push * 0.65);
  camera.lookAt(0, 0, 0);
  camera.updateProjectionMatrix();
  return null;
};

const Node: React.FC<{name: 'A' | 'B'; frame: number; fps: number}> = ({name, frame, fps}) => {
  const arrival = spring({frame: frame - 16, fps, config: {mass: 0.4, stiffness: 250, damping: 12}});
  const offset = 355 - arrival * 50;
  return <div style={{position:'absolute', top:844, left:'50%', width:232, height:232, marginLeft:-116,
    transform:`translateX(${name === 'A' ? -offset : offset}px)`, border:`1px solid ${LIME}`,
    borderRadius:'50%', boxShadow:'0 0 14px rgba(210,255,82,.32), inset 0 0 12px rgba(210,255,82,.12)',
    display:'flex', alignItems:'center', justifyContent:'center', color:WHITE, font:'700 29px Arial, sans-serif', letterSpacing:3}}>
    <div style={{position:'absolute', inset:12, border:`1px solid ${HUD}`, borderRadius:'50%'}} />
    <div style={{position:'absolute', inset:-8, transform:`rotate(${frame * (name === 'A' ? 0.8 : -0.8)}deg)`}}>
      <div style={{position:'absolute', left:'50%', top:0, width:2, height:15, background:LIME, boxShadow:'0 0 9px #D2FF52'}} />
      <div style={{position:'absolute', left:'50%', bottom:0, width:2, height:15, background:LIME}} />
    </div>
    <span>NODE {name}</span>
  </div>;
};

type Phrase = {start: number; end: number; words: {text: string; at: number}[]};
const phrases: Phrase[] = [
  {start:t.why, end:t.two, words:[{text:'WHY', at:t.why}, {text:'WOULD', at:t.would}]},
  {start:t.two, end:t.trade, words:[{text:'TWO', at:t.two}, {text:'COUNTRIES', at:t.countries}]},
  {start:t.trade, end:t.a, words:[{text:'TRADE', at:t.trade}, {text:'USING', at:t.using}]},
  {start:t.a, end:t.neither, words:[{text:'A', at:t.a}, {text:'CURRENCY', at:t.currency}]},
];
const PhraseType: React.FC<{phrase: Phrase; frame: number; fps: number}> = ({phrase, frame, fps}) => {
  if (frame < phrase.start || frame >= phrase.end) return null;
  return <div style={{position:'absolute', left:78, right:78, top:250, fontFamily:'Anton, Impact, sans-serif', lineHeight:0.97}}>
    {phrase.words.map(({text, at}) => {
      const progress = spring({frame:frame-at, fps, config:{mass:0.4, stiffness:250, damping:12}});
      const outgoing = lerp(frame, [phrase.end-3, phrase.end], [1,0]);
      return <div key={text} style={{fontSize:text.length > 8 ? 136 : 170, color:WHITE, opacity:(frame >= at ? 1 : 0)*outgoing,
        transform:`translate3d(0, ${(1-progress)*55}px, 0) scale(${0.85+0.15*progress})`, transformOrigin:'left center'}}>{text}</div>;
    })}
  </div>;
};

const Caption: React.FC<{frame: number}> = ({frame}) => {
  const rows = [
    [{word:'WHY', at:t.why}, {word:'WOULD', at:t.would}, {word:'TWO', at:t.two}, {word:'COUNTRIES', at:t.countries}, {word:'TRADE', at:t.trade}],
    [{word:'USING', at:t.using}, {word:'A', at:t.a}, {word:'CURRENCY', at:t.currency}, {word:'NEITHER', at:t.neither}, {word:'ONE', at:t.one}, {word:'ISSUES?', at:t.issues}],
  ];
  return <div style={{position:'absolute', left:70, right:70, bottom:210, background:VOID, border:`1px solid ${HUD}`,
    padding:'24px 12px', textAlign:'center', fontFamily:'Arial, sans-serif', fontWeight:700, fontSize:31, lineHeight:1.55, color:WHITE}}>
    {rows.map((row, i) => <div key={i}>{row.map(({word}, j) => <span key={word} style={{color:word === 'NEITHER' && frame >= t.neither ? LIME : WHITE}}>{word}{j < row.length-1 ? ' ' : ''}</span>)}</div>)}
  </div>;
};

/** Silent Scene 1 prototype. Every frame marker is estimated. */
export const Scene1: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const [fontHandle] = useState(() => delayRender('Load Anton for Scene 1'));
  useEffect(() => {document.fonts.load('100px Anton').then(() => continueRender(fontHandle)).catch(() => continueRender(fontHandle));}, [fontHandle]);
  const finalLine = spring({frame:frame-t.one, fps, config:{mass:0.4, stiffness:250, damping:12}});
  const issueLine = spring({frame:frame-t.issues, fps, config:{mass:0.4, stiffness:250, damping:12}});
  const beam = lerp(frame, [t.trade,t.currency], [0,1]);

  return <AbsoluteFill style={{overflow:'hidden', background:VOID}}>
    <style>{`@font-face { font-family: Anton; src: url('${staticFile('fonts/Anton-Regular.ttf')}'); }`}</style>
    <CinematicWord text="NEITHER" triggerFrame={t.neither} playImpactSound={false} accentMode="lime"
      textStyle={{fontFamily:'Anton, Impact, sans-serif', fontSize:182, position:'absolute', top:268, left:78, letterSpacing:'-0.01em', color:LIME}}>
      <CyberAtmosphere />
      <div style={{position:'absolute', left:116, right:116, top:959, height:1, background:HUD}}>
        <div style={{width:`${beam*100}%`, height:1, background:LIME, boxShadow:'0 0 8px #D2FF52', opacity:0.7}} />
      </div>
      <Node name="A" frame={frame} fps={fps} /><Node name="B" frame={frame} fps={fps} />
      <ThreeCanvas width={width} height={height} camera={{position:[0,0,10.4], fov:36, near:0.1, far:60}} gl={{alpha:true, antialias:true}}>
        <CameraRig frame={frame} fps={fps} /><Dollar frame={frame} />
      </ThreeCanvas>
      <div style={{position:'absolute', left:78, right:78, top:130, display:'flex', justifyContent:'space-between', font:'22px monospace', letterSpacing:3, color:WHITE}}><span>GLOBAL TRADE / 01</span><span>ILLUSTRATIVE</span></div>
      <div style={{position:'absolute', left:78, right:78, top:167, height:1, background:HUD}}><div style={{height:1, width:`${(frame/(SCENE_1_DURATION-1))*100}%`, background:LIME}} /></div>
      {phrases.map(phrase => <PhraseType key={phrase.start} phrase={phrase} frame={frame} fps={fps} />)}
      {frame >= t.one && <div style={{position:'absolute', left:78, top:480, fontFamily:'Anton, Impact, sans-serif', fontSize:150, lineHeight:1, color:WHITE,
        transform:`translateY(${(1-finalLine)*40}px) scale(${0.9+0.1*finalLine})`, transformOrigin:'left center'}}>ONE {frame >= t.issues && <span style={{display:'inline-block', transform:`translateY(${(1-issueLine)*40}px) scale(${0.9+0.1*issueLine})`, transformOrigin:'left center'}}>ISSUES?</span>}</div>}
      <div style={{position:'absolute', left:0, right:0, top:1255, textAlign:'center', color:WHITE, font:'21px monospace', letterSpacing:3}}>NODE A + NODE B / USD AS THE SHARED UNIT</div>
      <Caption frame={frame} />
      {frame >= 135 && [0,1,2].map(i => <div key={i} aria-hidden="true" style={{position:'absolute', top:`${25+i*24+((frame+i)%3)*2}%`, left:`${((frame-135)*29+i*31)%95-8}%`, width:`${23+i*8}%`, height:i===1?5:3, background:i===1?WHITE:LIME, opacity:0.6, pointerEvents:'none'}} />)}
    </CinematicWord>
    <AudioTrack />
  </AbsoluteFill>;
};
