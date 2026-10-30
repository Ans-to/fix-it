import React, {useEffect, useMemo, useState} from 'react';
import {AbsoluteFill, continueRender, delayRender, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';
import {Atmosphere} from '../components/Atmosphere';
import {CinematicWord} from '../components/CinematicWord';
import {AudioTrack} from '../audio/AudioTrack';
import {SCENE_1_DURATION, SCENE_1_TIMINGS as t} from '../config/mockTimings';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const lerp = (frame: number, input: number[], output: number[]) => interpolate(frame, input, output, clamp);

const makeLabel = (label: string) => {
  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext('2d');
  if (!ctx) throw new Error('Unable to create the procedural label texture.');
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = '#ecffcc';
  ctx.font = '800 270px sans-serif';
  ctx.fillText(label, 256, 260);
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  return texture;
};

const Marker: React.FC<{label: 'A' | 'B'; position: [number, number, number]; frame: number}> = ({label, position, frame}) => {
  const texture = useMemo(() => makeLabel(label), [label]);
  useEffect(() => () => texture.dispose(), [texture]);
  return (
    <group position={position} rotation={[0.1, label === 'A' ? 0.22 : -0.22, 0.05 * Math.sin(frame * 0.04)]}>
      <mesh><boxGeometry args={[0.68, 0.85, 0.20]} /><meshStandardMaterial color="#173d38" metalness={0.68} roughness={0.3} /></mesh>
      <mesh position={[0, 0, 0.103]}><planeGeometry args={[0.57, 0.73]} /><meshBasicMaterial color="#1f6255" /></mesh>
      <mesh position={[0, 0, 0.109]}><planeGeometry args={[0.46, 0.46]} /><meshBasicMaterial map={texture} transparent /></mesh>
      <mesh position={[0, -0.51, 0]} rotation={[Math.PI / 2, 0, 0]}><torusGeometry args={[0.52, 0.014, 8, 56]} /><meshBasicMaterial color="#b9ff73" transparent opacity={0.7} /></mesh>
    </group>
  );
};

const Dollar: React.FC<{position: [number, number, number]; frame: number}> = ({position, frame}) => {
  const texture = useMemo(() => makeLabel('$'), []);
  useEffect(() => () => texture.dispose(), [texture]);
  return (
    <group position={position} rotation={[0.16, 0.42 + frame * 0.035, 0.06]}>
      <mesh rotation={[Math.PI / 2, 0, 0]}><cylinderGeometry args={[0.43, 0.43, 0.16, 56]} /><meshStandardMaterial color="#c9c46b" metalness={0.8} roughness={0.24} /></mesh>
      <mesh position={[0, 0, 0.086]}><circleGeometry args={[0.40, 56]} /><meshStandardMaterial color="#c8c879" metalness={0.65} roughness={0.3} /></mesh>
      <mesh position={[0, 0, 0.09]}><planeGeometry args={[0.59, 0.59]} /><meshBasicMaterial map={texture} transparent /></mesh>
      <mesh position={[0, 0, -0.086]} rotation={[0, Math.PI, 0]}><circleGeometry args={[0.4, 56]} /><meshStandardMaterial color="#c8c879" metalness={0.65} roughness={0.3} /></mesh>
      <mesh position={[0, 0, -0.09]} rotation={[0, Math.PI, 0]}><planeGeometry args={[0.59, 0.59]} /><meshBasicMaterial map={texture} transparent /></mesh>
      <mesh rotation={[0.65, 0.2, frame * 0.025]}><torusGeometry args={[0.62, 0.012, 8, 72]} /><meshBasicMaterial color="#dfff80" transparent opacity={0.65} /></mesh>
    </group>
  );
};

const CameraRig: React.FC<{frame: number; fps: number}> = ({frame, fps}) => {
  const {camera} = useThree();
  const push = spring({frame: frame - 8, fps, config: {mass: 0.4, stiffness: 115, damping: 18}});
  camera.position.set(Math.sin(frame * 0.025) * 0.16, 0.12 + Math.cos(frame * 0.018) * 0.12, 10.4 - push * 0.65);
  camera.lookAt(0, -0.25, 0);
  camera.updateProjectionMatrix();
  return null;
};

const World: React.FC<{frame: number; fps: number}> = ({frame, fps}) => {
  const arrive = spring({frame: frame - 16, fps, config: {mass: 0.4, stiffness: 250, damping: 12}});
  const separation = 1.75 - arrive * 0.55;
  const travel = lerp(frame, [t.using, t.neither, 123], [0, 0.5, 1]);
  const x = -0.95 + travel * 1.9;
  const y = -0.30 + Math.sin(travel * Math.PI) * 0.25;
  const beam = lerp(frame, [t.trade, t.currency], [0, 1]);
  return (
    <>
      <CameraRig frame={frame} fps={fps} />
      <ambientLight intensity={1.1} />
      <directionalLight position={[3, 4, 6]} intensity={3.2} color="#e5ffcb" />
      <pointLight position={[-3, 1, 4]} intensity={18} color="#65ffc3" />
      <pointLight position={[3, 1, 3]} intensity={14} color="#dfff78" />
      <group position={[0, -0.45, 0]}>
        <Marker label="A" position={[-separation, 0.2, 0]} frame={frame} />
        <Marker label="B" position={[separation, 0.2, 0]} frame={frame} />
        <mesh position={[0, -0.31, -0.08]} scale={[beam, 1, 1]}>
          <boxGeometry args={[2.45, 0.018, 0.018]} /><meshBasicMaterial color="#b3ffb1" transparent opacity={0.75} />
        </mesh>
        <Dollar position={[x, y, 0.42]} frame={frame} />
        {[0, 1, 2].map((i) => (
          <mesh key={i} position={[0, 0, -0.8 - i * 0.12]} rotation={[0.4 + i * 0.2, frame * 0.012, frame * 0.012 + i]}>
            <torusGeometry args={[1.55 + i * 0.14, 0.008, 8, 72]} />
            <meshBasicMaterial color={i === 1 ? '#e6f58c' : '#54cdb3'} transparent opacity={0.24} />
          </mesh>
        ))}
        {Array.from({length: 30}, (_, i) => (
          <mesh key={i} position={[Math.sin(i * 8.7) * 1.9, Math.cos(i * 3.17) * 1.9, -1 - (i % 5) * 0.25]}>
            <sphereGeometry args={[i % 6 === 0 ? 0.022 : 0.012, 6, 6]} />
            <meshBasicMaterial color={i % 4 ? '#7eead5' : '#e5ff90'} transparent opacity={0.5} />
          </mesh>
        ))}
      </group>
    </>
  );
};

type Phrase = {start: number; end: number; words: {text: string; at: number}[]};
const phrases: Phrase[] = [
  {start: t.why, end: t.two, words: [{text: 'WHY', at: t.why}, {text: 'WOULD', at: t.would}]},
  {start: t.two, end: t.trade, words: [{text: 'TWO', at: t.two}, {text: 'COUNTRIES', at: t.countries}]},
  {start: t.trade, end: t.a, words: [{text: 'TRADE', at: t.trade}, {text: 'USING', at: t.using}]},
  {start: t.a, end: t.neither, words: [{text: 'A', at: t.a}, {text: 'CURRENCY', at: t.currency}]},
];

const PhraseType: React.FC<{phrase: Phrase; frame: number; fps: number}> = ({phrase, frame, fps}) => {
  if (frame < phrase.start || frame >= phrase.end) return null;
  return (
    <div style={{position: 'absolute', left: 78, right: 78, top: 250, fontFamily: 'Anton, Impact, sans-serif', lineHeight: 0.97, textShadow: '0 8px 35px rgba(0,0,0,.55)'}}>
      {phrase.words.map(({text, at}, i) => {
        const progress = spring({frame: frame - at, fps, config: {mass: 0.4, stiffness: 250, damping: 12}});
        const outgoing = lerp(frame, [phrase.end - 3, phrase.end], [1, 0]);
        return <div key={text} style={{fontSize: text.length > 8 ? 136 : 170, color: i === 0 ? '#f4ffe9' : '#dfff84', opacity: (frame >= at ? 1 : 0) * outgoing, transform: `translate3d(0, ${(1 - progress) * 55}px, 0) scale(${0.85 + 0.15 * progress})`, transformOrigin: 'left center'}}>{text}</div>;
      })}
    </div>
  );
};

const Caption: React.FC<{frame: number}> = ({frame}) => {
  const rows = [
    [{word: 'Why', at: t.why}, {word: 'would', at: t.would}, {word: 'two', at: t.two}, {word: 'countries', at: t.countries}, {word: 'trade', at: t.trade}],
    [{word: 'using', at: t.using}, {word: 'a', at: t.a}, {word: 'currency', at: t.currency}, {word: 'neither', at: t.neither}, {word: 'one', at: t.one}, {word: 'issues?', at: t.issues}],
  ];
  const flat = rows.flat();
  const current = flat.reduce((index, item, i) => frame >= item.at ? i : index, -1);
  let n = 0;
  return <div style={{position: 'absolute', left: 70, right: 70, bottom: 210, borderRadius: 12, background: 'rgba(6,16,22,.89)', border: '1px solid rgba(190,255,158,.22)', padding: '22px 12px', textAlign: 'center', fontFamily: 'Arial, sans-serif', fontWeight: 700, fontSize: 34, lineHeight: 1.45, color: '#edf9e7'}}>
    {rows.map((row, rowIndex) => <div key={rowIndex}>{row.map(({word}, i) => {const idx = n++; return <span key={word} style={{color: idx === current ? '#dfff86' : '#edf9e7'}}>{word}{i < row.length - 1 ? ' ' : ''}</span>;})}</div>)}
  </div>;
};

/** Silent prototype of approved scene 1. Every frame marker is estimated. */
export const Scene1: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const [fontHandle] = useState(() => delayRender('Load Anton for Scene 1'));
  useEffect(() => {
    document.fonts.load('100px Anton').then(() => continueRender(fontHandle)).catch(() => continueRender(fontHandle));
  }, [fontHandle]);
  const finalLine = spring({frame: frame - t.one, fps, config: {mass: 0.4, stiffness: 250, damping: 12}});
  const issueLine = spring({frame: frame - t.issues, fps, config: {mass: 0.4, stiffness: 250, damping: 12}});

  return <AbsoluteFill style={{overflow: 'hidden'}}>
    <style>{`@font-face { font-family: Anton; src: url('${staticFile('fonts/Anton-Regular.ttf')}'); }`}</style>
    <CinematicWord text="NEITHER" triggerFrame={t.neither} playImpactSound={false} textStyle={{fontFamily: 'Anton, Impact, sans-serif', fontSize: 182, position: 'absolute', top: 268, left: 78, letterSpacing: '-0.01em'}}>
      <Atmosphere durationInFrames={SCENE_1_DURATION} />
      <ThreeCanvas width={width} height={height} camera={{position: [0, 0, 10.4], fov: 36, near: 0.1, far: 60}} gl={{alpha: true, antialias: true}}>
        <World frame={frame} fps={fps} />
      </ThreeCanvas>
      <div style={{position: 'absolute', left: 78, right: 78, top: 130, display: 'flex', justifyContent: 'space-between', font: '22px monospace', letterSpacing: 3, color: '#c3e8b5'}}><span>GLOBAL TRADE / 01</span><span>ILLUSTRATIVE</span></div>
      <div style={{position: 'absolute', left: 78, right: 78, top: 167, height: 2, background: 'rgba(192,255,166,.18)'}}><div style={{height: 2, width: `${(frame / (SCENE_1_DURATION - 1)) * 100}%`, background: '#dfff84'}} /></div>
      {phrases.map((phrase) => <PhraseType key={phrase.start} phrase={phrase} frame={frame} fps={fps} />)}
      {frame >= t.one && <div style={{position: 'absolute', left: 78, top: 480, fontFamily: 'Anton, Impact, sans-serif', fontSize: 150, lineHeight: 1, color: '#dfff84', textShadow: '0 8px 30px rgba(0,0,0,.6)', transform: `translateY(${(1 - finalLine) * 40}px) scale(${0.9 + 0.1 * finalLine})`, transformOrigin: 'left center'}}>ONE {frame >= t.issues && <span style={{display: 'inline-block', transform: `translateY(${(1 - issueLine) * 40}px) scale(${0.9 + 0.1 * issueLine})`, transformOrigin: 'left center'}}>ISSUES?</span>}</div>}
      <div style={{position: 'absolute', left: 0, right: 0, top: 1370, textAlign: 'center', color: '#b8dfb2', font: '21px monospace', letterSpacing: 3}}>A + B  /  USD AS THE SHARED UNIT</div>
      <Caption frame={frame} />
      {frame >= 135 && [0, 1, 2].map((i) => <div key={i} aria-hidden="true" style={{position: 'absolute', top: `${25 + i * 24 + ((frame + i) % 3) * 2}%`, left: `${((frame - 135) * 29 + i * 31) % 95 - 8}%`, width: `${23 + i * 8}%`, height: i === 1 ? 5 : 3, background: i === 1 ? 'rgba(126,255,234,.65)' : 'rgba(255,91,141,.6)', boxShadow: '6px 0 rgba(109,148,255,.5)', pointerEvents: 'none'}} />)}
      {frame >= 135 && <div aria-hidden="true" style={{position: 'absolute', top: 0, bottom: 0, left: `${(frame - 135) * 17 - 40}%`, width: '24%', background: 'linear-gradient(90deg,transparent,rgba(222,255,132,.15),transparent)', transform: 'skewX(-12deg)', pointerEvents: 'none'}} />}
    </CinematicWord>
    <AudioTrack />
  </AbsoluteFill>;
};
