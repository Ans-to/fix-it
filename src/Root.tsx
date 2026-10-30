import React from 'react';
import {
  AbsoluteFill,
  Composition,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {
  OBSIDIAN_FOUNDATION,
  SAFETY_ORANGE_ACCENT,
  ELECTRIC_WHITE_FOREGROUND,
  CRIMSON_ALERT,
} from './colors.js';
import KineticEngine from './KineticEngine.jsx';
import { Starfield } from './Starfield.js';

// Constants based on exact specifications
const CANVAS_WIDTH = 1080;
const CANVAS_HEIGHT = 1920;
const FPS = 30;
const TOTAL_FRAMES = 1547; // Exactly 1,547 frames (51.57 seconds)

// Z-Index Layer Decoupling Mapping:
// zIndex: 1  -> Clean coordinate grid background
// zIndex: 10 -> Drifting starfield
// zIndex: 20 -> UI background widgets
// zIndex: 55 -> Hero kinetic typography text box
// zIndex: 65 -> Crimson diagnostic warning overlay (handled in ContextualUiSimulation)
// zIndex: 75 -> Telemetry HUD bars

// Full-bleed grid; the separately layered canvas supplies the moving stars.
export const CoordinateGridBackground: React.FC = () => (
  <AbsoluteFill
    style={{
      inset: 0,
      backgroundColor: OBSIDIAN_FOUNDATION,
      zIndex: 1,
      backgroundImage:
        `linear-gradient(to right, rgba(255, 255, 255, 0.05) 1px, transparent 1px), ` +
        `linear-gradient(to bottom, rgba(255, 255, 255, 0.05) 1px, transparent 1px)`,
      backgroundSize: '40px 40px',
    }}
  />
);

export const TelemetryHUDBars: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  // Dynamic HUD bar simulation
  const barWidth = (frame % 100) / 100 * width * 0.8;

  return (
    <AbsoluteFill style={{ inset: 0, zIndex: 75 }}>
      {/* Top HUD Bar */}
      <div
        style={{
          position: 'absolute',
          top: '5%',
          left: '10%',
          width: `${barWidth}px`,
          height: '12px',
          backgroundColor: CRIMSON_ALERT,
          boxShadow: `0 0 15px ${CRIMSON_ALERT}`,
        }}
      />
      {/* Bottom HUD Bar */}
      <div
        style={{
          position: 'absolute',
          bottom: '5%',
          left: '10%',
          width: `${barWidth * 0.7}px`,
          height: '8px',
          backgroundColor: SAFETY_ORANGE_ACCENT,
          boxShadow: `0 0 10px ${SAFETY_ORANGE_ACCENT}`,
        }}
      />
    </AbsoluteFill>
  );
};

export const VideoComposition: React.FC<{ hasVoiceover: boolean }> = ({ hasVoiceover }) => {
  return (
    <>
      <CoordinateGridBackground />
      <Starfield />
      <KineticEngine hasVoiceover={hasVoiceover} />
      <TelemetryHUDBars />
    </>
  );
};

// Root Configuration
export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="main-composition"
        component={VideoComposition}
        defaultProps={{ hasVoiceover: false }}
        width={CANVAS_WIDTH}
        height={CANVAS_HEIGHT}
        fps={FPS}
        durationInFrames={TOTAL_FRAMES}
      />
    </>
  );
};

export default Root;
