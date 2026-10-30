import React from 'react';
import { SCENE_STARTS } from './scene-starts.js';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {
  OBSIDIAN_FOUNDATION,
  SAFETY_ORANGE_ACCENT,
  ELECTRIC_WHITE_FOREGROUND,
  CRIMSON_ALERT,
} from './colors.js';
import wordCues from '../public/agent-engine/word-cues.json' with { type: 'json' };

// Define the type for word cues from JSON
interface WordCue {
  word: string;
  startFrame: number;
  endFrame: number;
  scene: string;
}

// Action-Verb Mapping Constants
const PROMPT_INPUT_WORDS = ['prompt', 'input', 'command', 'type', 'enter'];
const ARCHITECTURE_COMPILING_WORDS = ['architecture', 'compiling', 'pipeline', 'node', 'graph', 'execution', 'core', 'mechanism'];
const CONFLICT_BREAK_ERROR_WORDS = ['unexpected', 'shift', 'conflict', 'break', 'error', 'alert', 'crimson', 'warning'];

// Frosted Glassmorphism Style
const glassmorphismStyle = {
  backdropFilter: 'blur(12px)',
  border: '1px solid rgba(255, 255, 252, 0.1)',
  boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.8), inset 0 0 16px rgba(255, 69, 0, 0.1)',
  backgroundColor: 'rgba(11, 15, 25, 0.7)', // Obsidian Foundation with transparency
  borderRadius: '12px',
};

// 1. Live CLI/Prompt Box (Action-Verb: prompts/input)
interface CLITypewriterCardProps {
  frame: number;
  word: WordCue;
}

const CLITypewriterCard: React.FC<CLITypewriterCardProps> = ({ frame, word }) => {
  const { width } = useVideoConfig();
  
  // Character-accurate typing for CLI tokens
  const localFrame = frame - word.startFrame;
  const charsTyped = Math.max(0, Math.min(25, Math.floor(localFrame / 4))); // 25 chars max
  const typingTokens = [
    'agent-engine>',
    'compile --target=vertical',
    '--resolution=1080x1920',
    '--frames=1547',
    '--fps=30',
    '--sync=word-exact',
    '--motion=dynamic',
    '--profile=hook-climax',
    '--profile=code-typewriter',
    '--profile=metric-glitch',
    '--zero-dead-space=true',
    '--glassmorphism=enabled',
    '--diagnostic=active',
    '--stack-trace=live',
    '--execution=pipeline',
    '--node-graph=rendered',
    '--conflict-detection=on',
    '--resolution-achieved',
    '--final-conclusion',
    '--complete-success',
    '--system-ready',
    '--processing-complete',
    '--output-generated',
    '--session-terminated',
    '--exit-code=0',
  ];

  const currentTokenIndex = Math.min(typingTokens.length - 1, Math.floor(charsTyped / 15));
  const currentToken = typingTokens[currentTokenIndex] || '';
  const visibleChars = currentToken.substring(0, charsTyped % 15);
  
  // Blinking cursor
  const cursorVisible = Math.floor(localFrame / 10) % 2 === 0;

  const opacity = localFrame >= 0 && localFrame < (word.endFrame - word.startFrame) ? 1 : 0;

  return (
    <div
      style={{
        ...glassmorphismStyle,
        position: 'absolute',
        bottom: '15%',
        left: '10%',
        width: '35%',
        height: '18%',
        padding: '16px',
        fontFamily: 'monospace',
        fontSize: '18px',
        color: ELECTRIC_WHITE_FOREGROUND,
        opacity,
        transform: `scale(${0.9 + (opacity * 0.1)})`,
        transition: 'transform 0.3s ease',
      }}
    >
      <div style={{ color: SAFETY_ORANGE_ACCENT, marginBottom: '8px' }}>
        [SYSTEM] CLI SIMULATION ACTIVE
      </div>
      <div>{visibleChars}</div>
      {cursorVisible && opacity > 0 ? (
        <span style={{ color: SAFETY_ORANGE_ACCENT }}>_</span>
      ) : null}
    </div>
  );
};

// 2. Node-Graph Execution Pipeline Card (Action-Verb: architecture/compiling)
interface NodeGraphCardProps {
  frame: number;
  word: WordCue;
}

const NodeGraphCard: React.FC<NodeGraphCardProps> = ({ frame, word }) => {
  const { width, height } = useVideoConfig();
  const localFrame = frame - word.startFrame;
  
  // Pipeline progression animation
  const progress = Math.min(1, Math.max(0, localFrame / (word.endFrame - word.startFrame)));
  
  // Node positions (static but animated connections)
  const nodes = [
    { id: 'input', x: '10%', y: '30%', label: 'INPUT' },
    { id: 'process', x: '50%', y: '30%', label: 'PROCESS' },
    { id: 'compile', x: '90%', y: '30%', label: 'COMPILE' },
    { id: 'output', x: '50%', y: '70%', label: 'OUTPUT' },
  ];

  const opacity = localFrame >= 0 && localFrame < (word.endFrame - word.startFrame) ? 1 : 0;

  return (
    <div
      style={{
        ...glassmorphismStyle,
        position: 'absolute',
        top: '15%',
        right: '10%',
        width: '40%',
        height: '45%',
        padding: '20px',
        opacity,
        transform: `scale(${0.95 + (opacity * 0.05)})`,
        transition: 'transform 0.3s ease',
      }}
    >
      <div style={{ color: SAFETY_ORANGE_ACCENT, marginBottom: '12px', fontSize: '16px', fontWeight: 'bold' }}>
        NODE-GRAPH EXECUTION PIPELINE
      </div>
      
      {/* Node connections with progress animation */}
      <svg width="100%" height="80%" style={{ position: 'absolute', top: '40px', left: '0', pointerEvents: 'none' }}>
        {/* Connection lines */}
        <line x1="10%" y1="30%" x2="50%" y2="30%" stroke={SAFETY_ORANGE_ACCENT} strokeWidth="2" strokeDasharray="5,5" style={{ opacity: progress }} />
        <line x1="50%" y1="30%" x2="90%" y2="30%" stroke={SAFETY_ORANGE_ACCENT} strokeWidth="2" strokeDasharray="5,5" style={{ opacity: progress * 0.7 }} />
        <line x1="50%" y1="30%" x2="50%" y2="70%" stroke={SAFETY_ORANGE_ACCENT} strokeWidth="2" strokeDasharray="5,5" style={{ opacity: progress * 0.5 }} />
        
        {/* Node circles */}
        {nodes.map((node) => (
          <circle
            key={node.id}
            cx={node.x}
            cy={node.y}
            r="8"
            fill={ELECTRIC_WHITE_FOREGROUND}
            style={{ opacity: progress }}
          />
        ))}
      </svg>
      
      {/* Node labels */}
      {nodes.map((node) => (
        <div
          key={node.id}
          style={{
            position: 'absolute',
            left: node.x,
            top: node.y,
            transform: 'translate(-50%, -50%)',
            fontSize: '12px',
            color: ELECTRIC_WHITE_FOREGROUND,
            opacity: progress,
          }}
        >
          {node.label}
        </div>
      ))}
    </div>
  );
};

// 3. Crimson Diagnostic Warning Overlay (Action-Verb: conflict/break/error)
interface DiagnosticWarningOverlayProps {
  frame: number;
  word: WordCue;
}

const DiagnosticWarningOverlay: React.FC<DiagnosticWarningOverlayProps> = ({ frame, word }) => {
  const localFrame = frame - word.startFrame;
  const { width, height } = useVideoConfig();
  
  // Live stack trace simulation
  const stackTraces = [
    'ERROR: Unexpected logic shift detected',
    'STACK: at MechanismScene.tsx:45:12',
    'STACK: at KineticEngine.tsx:128:8',
    'STACK: at Root.tsx:89:4',
    'WARNING: State leakage prevention active',
    'CRITICAL: Transition reconfiguration required',
    'ALERT: Core mechanism engagement failed',
    'RESOLVED: Ultimate resolution achieved',
    'COMPLETE: Final conclusion processed',
  ];
  
  const traceIndex = Math.floor(localFrame / 15) % stackTraces.length;
  const currentTrace = stackTraces[traceIndex];
  
  // Glitch effect
  const glitchOffset = Math.sin(localFrame * 0.8) * 3;
  
  const opacity = localFrame >= 0 && localFrame < (word.endFrame - word.startFrame) ? 1 : 0;

  // Only render if conflict/break/error words are present (checked in parent)
  return (
    <AbsoluteFill style={{ inset: 0, zIndex: 65 }}>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundColor: 'rgba(225, 29, 72, 0.15)', // Crimson Alert with transparency
          boxShadow: `0 0 40px ${CRIMSON_ALERT}`,
          opacity,
          pointerEvents: 'none',
        }}
      >
        <div style={{ position: 'absolute', top: '30%', left: 0, width: '100%', textAlign: 'center', transform: `translateX(${glitchOffset}px)`, color: CRIMSON_ALERT, fontSize: '24px', fontWeight: 'bold' }}>
          DIAGNOSTIC WARNING: {word.word.toUpperCase()}
        </div>
        <div style={{ position: 'absolute', top: '33%', left: 0, width: '100%', color: ELECTRIC_WHITE_FOREGROUND, fontFamily: 'monospace', fontSize: '14px', textAlign: 'center' }}>
          {currentTrace}
        </div>
        {/* Volumetric shadow effect */}
        <div style={{
          position: 'absolute',
          top: '0',
          left: '0',
          width: '100%',
          height: '100%',
          boxShadow: `inset 0 0 100px ${CRIMSON_ALERT}`,
          opacity: 0.3,
        }} />
      </div>
    </AbsoluteFill>
  );
};

// Main Contextual Ui Simulation Component
interface ContextualUiSimulationProps {
  sceneName: string;
}

export const ContextualUiSimulation: React.FC<ContextualUiSimulationProps> = ({ sceneName }) => {
  const frame = useCurrentFrame() + (SCENE_STARTS[sceneName] ?? 0);
  
  // Filter words for current scene
  const sceneWords = wordCues.filter((word: WordCue) => word.scene === sceneName);
  
  // Find currently active word (frame within start/end)
  const activeWord = sceneWords.find(
    (word: WordCue) => frame >= word.startFrame && frame < word.endFrame
  );

  // Zero Dead Space: Only render active UI elements tied to narration
  if (!activeWord) return null;

  // Determine action-verb mapping
  const wordLower = activeWord.word.toLowerCase();
  const isPromptInput = PROMPT_INPUT_WORDS.some((verb) => wordLower.includes(verb));
  const isArchitectureCompiling = ARCHITECTURE_COMPILING_WORDS.some((verb) => wordLower.includes(verb));
  const isConflictBreakError = CONFLICT_BREAK_ERROR_WORDS.some((verb) => wordLower.includes(verb));

  return (
    <>
      <AbsoluteFill style={{ inset: 0, zIndex: 20, pointerEvents: 'none' }}>
      {/* Render appropriate UI component based on action-verb mapping */}
      {isPromptInput && <CLITypewriterCard frame={frame} word={activeWord} />}
      
      {isArchitectureCompiling && <NodeGraphCard frame={frame} word={activeWord} />}
      
      {/* Default fallback: subtle activity indicator tied to narration */}
      {!isPromptInput && !isArchitectureCompiling && !isConflictBreakError && (
        <div
          style={{
            position: 'absolute',
            bottom: '15%',
            left: 0,
            width: '100%',
            padding: '8px',
            fontSize: '14px',
            color: ELECTRIC_WHITE_FOREGROUND,
            opacity: 0.6,
            textAlign: 'center',
          }}
        >
          ACTIVE NARRATION: {activeWord.word.toUpperCase()}
        </div>
      )}
      </AbsoluteFill>
      {/* Diagnostic mounts independently above the hero text. */}
      {isConflictBreakError && <DiagnosticWarningOverlay frame={frame} word={activeWord} />}
    </>
  );
};

export default ContextualUiSimulation;
