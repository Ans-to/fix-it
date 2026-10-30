import React, {useId} from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';

/** A restrained HUD texture over a solid void-black foundation. */
export const CyberAtmosphere: React.FC = () => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const grid = `hud-${useId().replace(/[^a-zA-Z0-9_-]/g, '')}`;
  return <AbsoluteFill style={{background: '#050507', overflow: 'hidden', pointerEvents: 'none'}}>
    <svg aria-hidden="true" width={width} height={height} style={{position:'absolute', opacity: 0.42, transform:`translateY(${frame * 0.08}px)`}}>
      <defs><pattern id={grid} width="90" height="90" patternUnits="userSpaceOnUse">
        <path d="M 0 90 V 0 H 90" fill="none" stroke="#1E2229" strokeWidth="1" />
      </pattern></defs>
      <rect width={width} height={height} fill={`url(#${grid})`} />
    </svg>
    <div aria-hidden="true" style={{position:'absolute', left:'12%', right:'12%', top:'51%', height:1, background:'#1E2229'}} />
  </AbsoluteFill>;
};
