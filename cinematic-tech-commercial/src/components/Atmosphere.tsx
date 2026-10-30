import React, {useId} from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

export type AtmosphereProps = {
  /** Pass the scene's frame count when the atmosphere is inside a shorter Sequence. */
  durationInFrames?: number;
};

/**
 * Frame-driven background. The zoom affects the grid and glow, while the
 * vignette stays fixed to the viewport. Frame numbers are Sequence-relative.
 */
export const Atmosphere: React.FC<AtmosphereProps> = ({durationInFrames}) => {
  const frame = useCurrentFrame();
  const {durationInFrames: compositionDuration, fps, width, height} = useVideoConfig();
  const duration = durationInFrames ?? compositionDuration;
  if (!Number.isInteger(duration) || duration < 1) {
    throw new Error('Atmosphere durationInFrames must be a positive integer.');
  }

  const zoom = interpolate(frame, [0, Math.max(1, duration - 1)], [1, 1.05], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const pulse = (Math.sin((2 * Math.PI * frame) / (fps * 2.4)) + 1) / 2;
  // A unique pattern ID prevents multiple Atmosphere instances from colliding.
  const patternId = `cyber-grid-${useId().replace(/[^a-zA-Z0-9_-]/g, '')}`;

  return (
    <AbsoluteFill style={{overflow: 'hidden', pointerEvents: 'none'}}>
      <AbsoluteFill style={{transform: `scale(${zoom})`, transformOrigin: '50% 50%'}}>
        <AbsoluteFill
          style={{
            background:
              'radial-gradient(ellipse at 50% 47%, #1b3029 0%, #101c23 44%, #07101a 100%)',
          }}
        />
        <svg
          aria-hidden="true"
          viewBox={`0 0 ${width} ${height}`}
          preserveAspectRatio="none"
          style={{position: 'absolute', width: '100%', height: '100%', opacity: 0.34}}
        >
          <defs>
            <pattern id={patternId} width="64" height="64" patternUnits="userSpaceOnUse">
              <circle cx="32" cy="32" r="1.3" fill="#b8ffc3" opacity="0.65" />
              <path d="M 28 32 H 36 M 32 28 V 36" stroke="#caffb1" strokeWidth="0.55" opacity="0.35" />
            </pattern>
          </defs>
          <rect width={width} height={height} fill={`url(#${patternId})`} />
        </svg>
        <div
          aria-hidden="true"
          style={{
            position: 'absolute',
            left: '15%',
            top: '50%',
            width: '70%',
            aspectRatio: '1 / 1',
            borderRadius: '50%',
            background:
              'radial-gradient(circle, rgba(222,255,97,0.58) 0%, rgba(125,255,87,0.34) 30%, rgba(70,226,113,0.10) 55%, transparent 72%)',
            filter: 'blur(48px)',
            opacity: 0.48 + pulse * 0.24,
            transform: `translateY(-50%) scale(${0.92 + pulse * 0.14})`,
            transformOrigin: '50% 50%',
          }}
        />
      </AbsoluteFill>
      <AbsoluteFill
        aria-hidden="true"
        style={{
          background:
            'radial-gradient(ellipse at center, transparent 32%, rgba(2,7,13,0.3) 65%, rgba(2,7,13,0.83) 100%)',
        }}
      />
    </AbsoluteFill>
  );
};
