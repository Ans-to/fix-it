import React from 'react';
import {Audio, Sequence, staticFile, useVideoConfig} from 'remotion';

/** All timings are integer composition frames at 30 fps, with exclusive ends. */
export type SpeechRange = {
  startFrame: number;
  endFrame: number;
};

export type ImpactWord = 'neither' | 'only' | 'leading' | '1944';
export type ImpactCue = {
  word: ImpactWord;
  frame: number;
};

export type AudioTrackProps = {
  /** Measured voice-active ranges covering the complete narration, in composition frames. */
  speechRanges: readonly SpeechRange[];
  /** Verified word-onset frames for all impact words in storyboard.json. */
  impactCues: readonly ImpactCue[];
  /** Composition frame at which the beginning of voiceover.mp3 is placed. */
  voiceoverStartFrame?: number;
  bgmVolume?: number;
  voiceoverVolume?: number;
  whooshVolume?: number;
  subDropVolume?: number;
};

const IMPACT_WORDS: readonly ImpactWord[] = ['neither', 'only', 'leading', '1944'];
const DUCK_GAIN = 10 ** (-8 / 20);

const assertFrame = (value: number, label: string, maxExclusive: number) => {
  if (!Number.isInteger(value) || value < 0 || value >= maxExclusive) {
    throw new Error(`${label} must be an integer in [0, ${maxExclusive}).`);
  }
};

const assertVolume = (value: number, label: string) => {
  if (!Number.isFinite(value) || value < 0 || value > 1) {
    throw new Error(`${label} must be between 0 and 1.`);
  }
};

/** Build full-coverage constant-gain segments from voice-active ranges. */
export const buildMusicSegments = (
  durationInFrames: number,
  speechRanges: readonly SpeechRange[],
  bgmVolume: number,
) => {
  const boundaries = Array.from(new Set([
    0,
    durationInFrames,
    ...speechRanges.flatMap(({startFrame, endFrame}) => [startFrame, endFrame]),
  ])).sort((a, b) => a - b);
  const segments = boundaries.slice(0, -1).map((startFrame, i) => {
    const endFrame = boundaries[i + 1];
    const speaking = speechRanges.some((range) => startFrame >= range.startFrame && startFrame < range.endFrame);
    return {startFrame, endFrame, volume: bgmVolume * (speaking ? DUCK_GAIN : 1)};
  });
  return segments.reduce<typeof segments>((merged, segment) => {
    const previous = merged[merged.length - 1];
    if (previous && previous.endFrame === segment.startFrame && previous.volume === segment.volume) {
      previous.endFrame = segment.endFrame;
    } else {
      merged.push({...segment});
    }
    return merged;
  }, []);
};

/**
 * Mount once at composition root. Ranges and cues use composition-frame time;
 * no storyboard duration can substitute for measuring the actual narration.
 *
 * Use playImpactSound={false} on CinematicWord when AudioTrack handles SFX,
 * so a sub-drop is not played twice. This component does not supply the files
 * or determine the speech/word timings automatically.
 */
export const AudioTrack: React.FC<AudioTrackProps> = ({
  speechRanges,
  impactCues,
  voiceoverStartFrame = 0,
  bgmVolume = 0.25,
  voiceoverVolume = 1,
  whooshVolume = 0.4,
  subDropVolume = 0.65,
}) => {
  const {fps, durationInFrames} = useVideoConfig();
  if (fps !== 30) {
    throw new Error('AudioTrack timings are specified at 30 fps.');
  }
  assertFrame(voiceoverStartFrame, 'voiceoverStartFrame', durationInFrames);
  assertVolume(bgmVolume, 'bgmVolume');
  assertVolume(voiceoverVolume, 'voiceoverVolume');
  assertVolume(whooshVolume, 'whooshVolume');
  assertVolume(subDropVolume, 'subDropVolume');
  if (speechRanges.length === 0) {
    throw new Error('Provide measured speechRanges; the VO-active frames are unknown.');
  }
  for (const [i, range] of speechRanges.entries()) {
    assertFrame(range.startFrame, `speechRanges[${i}].startFrame`, durationInFrames);
    if (!Number.isInteger(range.endFrame) || range.endFrame <= range.startFrame || range.endFrame > durationInFrames) {
      throw new Error(`speechRanges[${i}].endFrame must be after its start and at most ${durationInFrames}.`);
    }
    if (range.startFrame < voiceoverStartFrame) {
      throw new Error(`speechRanges[${i}] starts before the voiceover.`);
    }
  }
  const seen = new Set<ImpactWord>();
  const frameByWord = new Map<ImpactWord, number>();
  for (const [i, cue] of impactCues.entries()) {
    assertFrame(cue.frame, `impactCues[${i}].frame`, durationInFrames);
    if (!IMPACT_WORDS.includes(cue.word) || seen.has(cue.word)) {
      throw new Error(`Unexpected or duplicate impact word: ${cue.word}.`);
    }
    if (cue.frame < voiceoverStartFrame) {
      throw new Error(`Impact word ${cue.word} occurs before the voiceover.`);
    }
    seen.add(cue.word);
    frameByWord.set(cue.word, cue.frame);
  }
  if (seen.size !== IMPACT_WORDS.length) {
    const missing = IMPACT_WORDS.filter((word) => !seen.has(word));
    throw new Error(`Provide one verified frame for each impact word. Missing: ${missing.join(', ')}.`);
  }

  for (let i = 1; i < IMPACT_WORDS.length; i++) {
    if (frameByWord.get(IMPACT_WORDS[i])! <= frameByWord.get(IMPACT_WORDS[i - 1])!) {
      throw new Error('Impact cues must follow the approved script order.');
    }
  }

  // Separate constant-volume segments avoid Remotion's rounding of animated
  // volume curves during FFmpeg rendering. trimBefore maintains music position.
  // The BGM file must cover the composition; it is not silently looped.
  const segments = buildMusicSegments(durationInFrames, speechRanges, bgmVolume);

  return (
    <>
      {segments.map(({startFrame, endFrame, volume}) => (
        <Sequence key={startFrame} from={startFrame} durationInFrames={endFrame - startFrame} layout="none">
          <Audio src={staticFile('bgm.mp3')} trimBefore={startFrame} volume={volume} />
        </Sequence>
      ))}
      <Sequence from={voiceoverStartFrame} layout="none">
        <Audio src={staticFile('voiceover.mp3')} volume={voiceoverVolume} />
      </Sequence>
      {impactCues.map(({word, frame}) => (
        <Sequence key={word} from={frame} layout="none">
          <Audio src={staticFile('whoosh.mp3')} volume={whooshVolume} />
          <Audio src={staticFile('sub_drop.mp3')} volume={subDropVolume} />
        </Sequence>
      ))}
    </>
  );
};
