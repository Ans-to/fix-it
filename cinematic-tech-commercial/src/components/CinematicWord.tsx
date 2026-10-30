import React, {type CSSProperties, type ReactNode} from 'react';
import {AbsoluteFill, Audio, random, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

export type CinematicWordProps = {
  text: string;
  /** Hit frame relative to the current Sequence, not necessarily the composition. */
  triggerFrame: number;
  /** Asset path relative to public/, e.g. 'sub_drop.mp3' (not a resolved URL). */
  impactSoundSrc?: string;
  /** Set false when ProductionAudioTrack triggers all impact sounds centrally. */
  playImpactSound?: boolean;
  /** Put every visible scene layer here so the entire viewport shakes together. */
  children: ReactNode;
  impactVolume?: number;
  /** Seed disambiguates repeated words while keeping renders deterministic. */
  seed?: string;
  shakePixels?: number;
  textStyle?: CSSProperties;
  /** Palette-safe impact styling for the minimalist cyber-editorial scene. */
  accentMode?: 'default' | 'lime';
};

/**
 * Impact word and viewport wrapper. Only children of this component are shaken;
 * mount all scene visuals inside it, not as siblings. By default an audio
 * source is required. Disable its sound when using the central ProductionAudioTrack,
 * which triggers the sub-drop, to avoid doubling the effect.
 */
export const CinematicWord: React.FC<CinematicWordProps> = ({
  text,
  triggerFrame,
  impactSoundSrc,
  playImpactSound = true,
  children,
  impactVolume = 1,
  seed = 'cinematic-word',
  shakePixels = 14,
  textStyle,
  accentMode = 'default',
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (!Number.isInteger(triggerFrame) || triggerFrame < 0) {
    throw new Error('CinematicWord triggerFrame must be a non-negative integer.');
  }
  if (playImpactSound && !impactSoundSrc) {
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
                textShadow: accentMode === 'lime'
                  ? '-3px 0 0 rgba(255,255,255,0.65), 3px 0 0 rgba(210,255,82,0.9), 0 0 22px rgba(210,255,82,0.9), 0 0 70px rgba(210,255,82,0.65)'
                  : '-5px 0 0 rgba(255,55,85,0.85), 0 -1px 0 rgba(118,255,92,0.9), 5px 0 0 rgba(58,132,255,0.85), 0 0 14px rgba(181,255,100,0.95), 0 0 36px rgba(122,255,104,0.65)',
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
          style={{backgroundColor: accentMode === 'lime' ? '#FFFFFF' : '#f7fff1', opacity: accentMode === 'lime' ? 0.16 : 0.3, pointerEvents: 'none'}}
        />
      )}
      {playImpactSound && impactSoundSrc && (
        <Sequence from={triggerFrame} layout="none">
          <Audio src={staticFile(impactSoundSrc)} volume={impactVolume} />
        </Sequence>
      )}
    </AbsoluteFill>
  );
};
