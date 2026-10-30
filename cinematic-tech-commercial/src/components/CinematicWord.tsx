import React, {type CSSProperties, type ReactNode} from 'react';
import {AbsoluteFill, Audio, random, Sequence, spring, useCurrentFrame, useVideoConfig} from 'remotion';

export type CinematicWordProps = {
  text: string;
  /** Hit frame relative to the current Sequence, not necessarily the composition. */
  triggerFrame: number;
  /** A licensed/local sub-bass asset, e.g. staticFile('audio/impact.wav'). */
  impactSoundSrc: string;
  /** Put every visible scene layer here so the entire viewport shakes together. */
  children: ReactNode;
  impactVolume?: number;
  /** Seed disambiguates repeated words while keeping renders deterministic. */
  seed?: string;
  shakePixels?: number;
  textStyle?: CSSProperties;
};

/**
 * Impact word and viewport wrapper. Only children of this component are shaken;
 * mount all scene visuals inside it, not as siblings. The audio source is
 * required, but the component does not provide or verify a sub-bass asset.
 */
export const CinematicWord: React.FC<CinematicWordProps> = ({
  text,
  triggerFrame,
  impactSoundSrc,
  children,
  impactVolume = 1,
  seed = 'cinematic-word',
  shakePixels = 14,
  textStyle,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (!Number.isInteger(triggerFrame) || triggerFrame < 0) {
    throw new Error('CinematicWord triggerFrame must be a non-negative integer.');
  }
  if (!impactSoundSrc) {
    throw new Error('CinematicWord requires a sub-bass impactSoundSrc.');
  }
  if (!Number.isFinite(shakePixels) || shakePixels <= 0) {
    throw new Error('CinematicWord shakePixels must be a positive number.');
  }
  if (!Number.isFinite(impactVolume) || impactVolume < 0 || impactVolume > 1) {
    throw new Error('CinematicWord impactVolume must be between 0 and 1.');
  }

  const elapsed = frame - triggerFrame;
  const isShaking = elapsed >= 0 && elapsed < 5;
  const strength = isShaking ? shakePixels * (1 - elapsed / 5) : 0;
  // Seeded by the local frame rather than Math.random(), so seeking and
  // parallel rendering reproduce the same five offsets in any frame order.
  const x = isShaking ? (random(`${seed}:${triggerFrame}:${elapsed}:x`) * 2 - 1) * strength : 0;
  const y = isShaking ? (random(`${seed}:${triggerFrame}:${elapsed}:y`) * 2 - 1) * strength : 0;
  const progress = spring({
    frame: Math.max(0, elapsed),
    fps,
    config: {mass: 0.4, stiffness: 250, damping: 12},
  });
  const scale = 0.72 + 0.28 * progress;
  const rise = (1 - progress) * 42;

  return (
    <AbsoluteFill style={{overflow: 'hidden', isolation: 'isolate'}}>
      <AbsoluteFill style={{transform: `translate3d(${x}px, ${y}px, 0)`}}>
        {children}
        {elapsed >= 0 && (
          <AbsoluteFill
            style={{display: 'flex', alignItems: 'center', justifyContent: 'center', pointerEvents: 'none'}}
          >
            <span
              style={{
                color: '#f8ffe8',
                fontFamily: 'Impact, sans-serif',
                fontWeight: 900,
                fontSize: 'clamp(48px, 13vw, 220px)',
                lineHeight: 1,
                letterSpacing: '-0.025em',
                textAlign: 'center',
                maxWidth: '90%',
                overflowWrap: 'anywhere',
                ...textStyle,
                transform: `translate3d(0, ${rise}px, 0) scale(${scale})`,
                textShadow:
                  '-5px 0 0 rgba(255,55,85,0.85), 0 -1px 0 rgba(118,255,92,0.9), 5px 0 0 rgba(58,132,255,0.85), 0 0 14px rgba(181,255,100,0.95), 0 0 36px rgba(122,255,104,0.65)',
              }}
            >
              {text}
            </span>
          </AbsoluteFill>
        )}
      </AbsoluteFill>
      {elapsed === 0 && (
        <AbsoluteFill
          aria-hidden="true"
          style={{backgroundColor: '#f7fff1', opacity: 0.3, pointerEvents: 'none'}}
        />
      )}
      <Sequence from={triggerFrame} layout="none">
        <Audio src={impactSoundSrc} volume={impactVolume} />
      </Sequence>
    </AbsoluteFill>
  );
};
