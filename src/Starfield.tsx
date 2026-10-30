import React, { useLayoutEffect, useRef } from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { ELECTRIC_WHITE_FOREGROUND, SAFETY_ORANGE_ACCENT } from './colors.js';

// Stable seeds, so the same frame renders identically regardless of render order.
const stars = Array.from({ length: 150 }, (_, index) => ({
  x: ((index * 73 + 19) % 151) / 151,
  y: ((index * 97 + 43) % 157) / 157,
  speed: 7 + (index % 9) * 1.8,
  drift: 2 + (index % 5) * 0.9,
  radius: index % 13 === 0 ? 2.6 : index % 4 === 0 ? 1.8 : 1.1,
  opacity: index % 13 === 0 ? 0.7 : index % 4 === 0 ? 0.5 : 0.32,
  orange: index % 11 === 0,
}));

export const Starfield: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  useLayoutEffect(() => {
    const context = canvasRef.current?.getContext('2d');
    if (!context) return;
    context.clearRect(0, 0, width, height);
    const seconds = frame / fps;
    for (const star of stars) {
      // Wrapping keeps the moving field full-bleed for the entire composition.
      const x = (star.x * width + seconds * star.drift) % width;
      const y = (star.y * height + seconds * star.speed) % height;
      context.globalAlpha = star.opacity;
      context.fillStyle = star.orange ? SAFETY_ORANGE_ACCENT : ELECTRIC_WHITE_FOREGROUND;
      context.beginPath();
      context.arc(x, y, star.radius, 0, Math.PI * 2);
      context.fill();
    }
    context.globalAlpha = 1;
  }, [frame, fps, width, height]);

  return (
    <AbsoluteFill style={{ inset: 0, zIndex: 10, pointerEvents: 'none', overflow: 'hidden' }}>
      <canvas ref={canvasRef} width={width} height={height} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }} />
    </AbsoluteFill>
  );
};
