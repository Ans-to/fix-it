import React from 'react';
import { SCENE_STARTS } from './scene-starts.js';
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  Audio,
  spring,
  staticFile,
} from 'remotion';
import {
  SAFETY_ORANGE_ACCENT,
  ELECTRIC_WHITE_FOREGROUND,
  CRIMSON_ALERT,
} from './colors.js';
import wordCues from '../public/agent-engine/word-cues.json' with { type: 'json' };
import ContextualUiSimulation from './ContextualUiSimulation.jsx';

// Define the type for word cues from JSON
interface WordCue {
  word: string;
  startFrame: number;
  endFrame: number;
  scene: string;
}

// Motion Profile 1: hook-climax (Heavy high-velocity spring impact)
interface HookClimaxMotionProps {
  word: WordCue;
  frame: number;
  index: number;
}

const HookClimaxMotion: React.FC<HookClimaxMotionProps> = ({ word, frame, index }) => {
  // Staggered token-level delay: 5 frames per word offset
  const delay = index * 5;
  const localFrame = frame - word.startFrame - delay;
  
  // Start the word on its cue; stagger only the impact animation, not the text.
  const { fps, width } = useVideoConfig();
  const springValue = spring({
    fps,
    frame: Math.max(0, localFrame),
    config: { stiffness: 300, damping: 10 },
  });
  const translateY = -(1 - springValue) * width * 0.12;
  const scale = 1 + (1 - springValue) * 0.35;

  return (
    <span
      style={{
        display: 'inline-block',
        margin: '0 8px',
        transform: `translateY(${translateY}px) scale(${scale})`,
        color:
          frame >= word.startFrame && frame < word.endFrame
            ? SAFETY_ORANGE_ACCENT
            : ELECTRIC_WHITE_FOREGROUND,
        transition: 'color 0.1s ease',
        opacity: frame >= word.startFrame ? 1 : 0,
      }}
    >
      {word.word}
    </span>
  );
};

// Motion Profile 2: code-typewriter (Character-accurate typing with blinking cursor)
interface CodeTypewriterMotionProps {
  word: WordCue;
  frame: number;
  index: number;
}

const CodeTypewriterMotion: React.FC<CodeTypewriterMotionProps> = ({ word, frame, index }) => {
  // The first character appears at the spoken onset; the rest are typed over
  // the measured word duration. Stagger the cursor effect, not the cue itself.
  const localFrame = frame - word.startFrame;
  const duration = Math.max(1, word.endFrame - word.startFrame);
  const charsTyped = localFrame < 0 ? 0 : Math.min(word.word.length,
    1 + Math.floor((localFrame / duration) * word.word.length));
  const visibleText = word.word.substring(0, charsTyped);
  const cursorVisible = Math.floor((localFrame - index * 8) / 15) % 2 === 0;
  const opacity = frame >= word.startFrame ? 1 : 0;

  return (
    <span
      style={{
        display: 'inline-block',
        margin: '0 8px',
        fontFamily: 'monospace',
        color: ELECTRIC_WHITE_FOREGROUND,
        opacity,
      }}
    >
      {visibleText}
      {cursorVisible && localFrame >= 0 && charsTyped === word.word.length ? (
        <span style={{ color: SAFETY_ORANGE_ACCENT }}>_</span>
      ) : null}
    </span>
  );
};

// Motion Profile 3: metric-glitch (Sharp digital scanline snap and chromatic aberration)
interface MetricGlitchMotionProps {
  word: WordCue;
  frame: number;
  index: number;
}

const MetricGlitchMotion: React.FC<MetricGlitchMotionProps> = ({ word, frame, index }) => {
  // Staggered token-level delay: 10 frames per word offset
  const delay = index * 10;
  const localFrame = frame - word.startFrame - delay;
  
  // Sharp digital scanline snap: every 10 frames
  const scanlineOffset = Math.floor(localFrame / 10) % 2 === 0 ? 2 : -2;
  
  // Chromatic aberration offset: random jitter every 5 frames
  const aberrationX = (Math.sin(localFrame * 0.5) * 3) * (localFrame % 5 === 0 ? 1 : 0);
  const aberrationY = (Math.cos(localFrame * 0.3) * 2) * (localFrame % 5 === 0 ? 1 : 0);
  
  const opacity = frame >= word.startFrame ? 1 : 0;

  return (
    <span
      style={{
        display: 'inline-block',
        margin: '0 8px',
        transform: `translateY(${scanlineOffset}px) translateX(${aberrationX}px)`,
        color:
          frame >= word.startFrame && frame < word.endFrame
            ? CRIMSON_ALERT
            : ELECTRIC_WHITE_FOREGROUND,
        textShadow: localFrame % 5 === 0
          ? `2px 0px ${SAFETY_ORANGE_ACCENT}, -2px 0px ${ELECTRIC_WHITE_FOREGROUND}`
          : 'none',
        opacity,
        filter: localFrame % 5 === 0 ? 'contrast(1.2)' : 'none',
      }}
    >
      {word.word}
    </span>
  );
};

// Helper component for word-exact synchronization with Anti-Pre-view Rule and Motion Profiles
interface WordSynchronizerProps {
  sceneName: string;
}

const WordSynchronizer: React.FC<WordSynchronizerProps> = ({ sceneName }) => {
  const frame = useCurrentFrame() + (SCENE_STARTS[sceneName] ?? 0);
  const { width, height } = useVideoConfig();

  // Filter words for current scene and apply Anti-Pre-view Rule
  const sceneWords = wordCues.filter((word: WordCue) => word.scene === sceneName);
  
  // Anti-Pre-view Rule: frame >= word.startFrame
  // Words accumulate strictly as they are spoken
  const accumulatedWords = sceneWords.filter(
    (word: WordCue) => frame >= word.startFrame
  );

  // Determine motion profile based on scene
  const getMotionComponent = (word: WordCue, index: number) => {
    switch (sceneName) {
      case 'HookScene':
        return <HookClimaxMotion word={word} frame={frame} index={index} />;
      case 'TwistScene':
        return <CodeTypewriterMotion word={word} frame={frame} index={index} />;
      case 'ShiftScene':
        return <MetricGlitchMotion word={word} frame={frame} index={index} />;
      case 'MechanismScene':
        return <HookClimaxMotion word={word} frame={frame} index={index} />; // Alternate pattern
      case 'PayoffScene':
        return <CodeTypewriterMotion word={word} frame={frame} index={index} />; // Alternate pattern
      case 'OutroScene':
        return <MetricGlitchMotion word={word} frame={frame} index={index} />; // Alternate pattern
      default:
        return <span>{word.word}</span>;
    }
  };

  return (
    <AbsoluteFill style={{ inset: 0, zIndex: 55, display: 'flex', justifyContent: 'center', alignItems: 'center', pointerEvents: 'none' }}>
      <div
        style={{
          width: '100%',
          transformOrigin: 'center center',
          color: ELECTRIC_WHITE_FOREGROUND,
          fontSize: Math.min(width * 0.085, height * 0.06),
          fontWeight: 'bold',
          textAlign: 'center',
          fontFamily: 'sans-serif',
          textTransform: 'uppercase',
          letterSpacing: '2px',
          opacity: accumulatedWords.length > 0 ? 1 : 0,
        }}
      >
        {accumulatedWords.filter(
          (word: WordCue) => frame >= word.startFrame
        ).map((word: WordCue, index: number) => (
          <React.Fragment key={index}>
            {getMotionComponent(word, index)}
          </React.Fragment>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// Isolated Scene Components with complete unmounting
export const HookScene: React.FC = () => {
  return (
    <AbsoluteFill style={{ inset: 0 }}>
      <WordSynchronizer sceneName="HookScene" />
      {/* Contextual UI Simulation */}
      <ContextualUiSimulation sceneName="HookScene" />
      {/* Telemetry HUD for Hook */}
      <AbsoluteFill style={{ zIndex: 75 }}>
        <div
          style={{
            position: 'absolute',
            top: '5%',
            left: '5%',
            width: '10%',
            height: '2px',
            backgroundColor: CRIMSON_ALERT,
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const TwistScene: React.FC = () => {
  return (
    <AbsoluteFill style={{ inset: 0 }}>
      <WordSynchronizer sceneName="TwistScene" />
      {/* Contextual UI Simulation */}
      <ContextualUiSimulation sceneName="TwistScene" />
      {/* Telemetry HUD for Twist */}
      <AbsoluteFill style={{ zIndex: 75 }}>
        <div
          style={{
            position: 'absolute',
            top: '10%',
            right: '5%',
            width: '2px',
            height: '10%',
            backgroundColor: CRIMSON_ALERT,
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const ShiftScene: React.FC = () => {
  return (
    <AbsoluteFill style={{ inset: 0 }}>
      <WordSynchronizer sceneName="ShiftScene" />
      {/* Contextual UI Simulation */}
      <ContextualUiSimulation sceneName="ShiftScene" />
      {/* Telemetry HUD for Shift */}
      <AbsoluteFill style={{ zIndex: 75 }}>
        <div
          style={{
            position: 'absolute',
            bottom: '5%',
            left: '5%',
            width: '15%',
            height: '2px',
            backgroundColor: CRIMSON_ALERT,
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const MechanismScene: React.FC = () => {
  return (
    <AbsoluteFill style={{ inset: 0 }}>
      <WordSynchronizer sceneName="MechanismScene" />
      {/* Contextual UI Simulation */}
      <ContextualUiSimulation sceneName="MechanismScene" />
      {/* Telemetry HUD for Mechanism */}
      <AbsoluteFill style={{ zIndex: 75 }}>
        <div
          style={{
            position: 'absolute',
            top: '5%',
            right: '5%',
            width: '15%',
            height: '2px',
            backgroundColor: CRIMSON_ALERT,
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const PayoffScene: React.FC = () => {
  return (
    <AbsoluteFill style={{ inset: 0 }}>
      <WordSynchronizer sceneName="PayoffScene" />
      {/* Contextual UI Simulation */}
      <ContextualUiSimulation sceneName="PayoffScene" />
      {/* Telemetry HUD for Payoff */}
      <AbsoluteFill style={{ zIndex: 75 }}>
        <div
          style={{
            position: 'absolute',
            bottom: '10%',
            right: '5%',
            width: '20%',
            height: '2px',
            backgroundColor: CRIMSON_ALERT,
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const OutroScene: React.FC = () => {
  return (
    <AbsoluteFill style={{ inset: 0 }}>
      <WordSynchronizer sceneName="OutroScene" />
      {/* Contextual UI Simulation */}
      <ContextualUiSimulation sceneName="OutroScene" />
      {/* Telemetry HUD for Outro */}
      <AbsoluteFill style={{ zIndex: 75 }}>
        <div
          style={{
            position: 'absolute',
            top: '5%',
            left: '50%',
            transform: 'translateX(-50%)',
            width: '10%',
            height: '2px',
            backgroundColor: CRIMSON_ALERT,
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// Main Kinetic Engine Component with Sequence Mapping
export const KineticEngine: React.FC<{ hasVoiceover: boolean }> = ({ hasVoiceover }) => {
  const { durationInFrames } = useVideoConfig();

  // Calculate scene durations based on word cues
  const hookDuration = 180; // Frames 0-180
  const twistDuration = 150; // Frames 180-330
  const shiftDuration = 180; // Frames 330-510
  const mechanismDuration = 210; // Frames 510-720
  const payoffDuration = 180; // Frames 720-900
  const outroDuration = durationInFrames - 900; // Frames 900-1547

  return (
    <>
      {/* Audio Track */}
      {hasVoiceover && <Audio src={staticFile("agent-engine/voiceover.wav")} volume={1} />}

      {/* Scene Sequences with complete unmounting */}
      <Sequence from={0} durationInFrames={hookDuration}>
        <HookScene />
      </Sequence>

      <Sequence from={hookDuration} durationInFrames={twistDuration}>
        <TwistScene />
      </Sequence>

      <Sequence
        from={hookDuration + twistDuration}
        durationInFrames={shiftDuration}
      >
        <ShiftScene />
      </Sequence>

      <Sequence
        from={hookDuration + twistDuration + shiftDuration}
        durationInFrames={mechanismDuration}
      >
        <MechanismScene />
      </Sequence>

      <Sequence
        from={hookDuration + twistDuration + shiftDuration + mechanismDuration}
        durationInFrames={payoffDuration}
      >
        <PayoffScene />
      </Sequence>

      <Sequence
        from={
          hookDuration +
          twistDuration +
          shiftDuration +
          mechanismDuration +
          payoffDuration
        }
        durationInFrames={outroDuration}
      >
        <OutroScene />
      </Sequence>
    </>
  );
};

export default KineticEngine;
