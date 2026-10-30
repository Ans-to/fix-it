/** Generate a reproducible local Piper voiceover and sample-derived word cues.
 * Requires piper-tts and a compatible Piper voice model (see README).
 */
import { spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync, writeFileSync, mkdirSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const fps = 30;
const durationFrames = 1547;
const scenes = JSON.parse(readFileSync(path.join(root, 'scripts/narration.json'), 'utf8'));
const model = process.env.PIPER_MODEL;
const config = process.env.PIPER_CONFIG || (model && `${model}.json`);
const python = process.env.PIPER_PYTHON || 'python3';
if (!model || !config) throw new Error('Set PIPER_MODEL and PIPER_CONFIG to your Piper ONNX voice and config. See README.');

// Generate individual words: their audio boundaries are measurable rather than
// guessed from character counts. A short gap separates adjacent spoken words.
const words = scenes.flatMap((scene) => scene.text.trim().split(/\s+/));
const temp = mkdtempSync(path.join(os.tmpdir(), 'agent-voiceover-'));
try {
  const result = spawnSync(python, [path.join(root, 'scripts/piper_synthesize.py'), model, config, temp], {
    input: JSON.stringify(words), encoding: 'utf8', maxBuffer: 10 * 1024 * 1024,
  });
  if (result.error || result.status !== 0) throw new Error(`Piper synthesis failed: ${result.error || result.stderr}`);

  const clips = words.map((_, i) => readWav(path.join(temp, `${i}.wav`)));
  const sampleRate = clips[0].sampleRate;
  if (sampleRate % fps || clips.some(c => c.sampleRate !== sampleRate)) throw new Error('Expected a consistent sample rate divisible by 30.');
  const samplesPerFrame = sampleRate / fps;
  const audio = Buffer.alloc(durationFrames * samplesPerFrame * 2);
  const cues = [];
  let clipIndex = 0;
  for (const scene of scenes) {
    let pos = (scene.startFrame + 9) * samplesPerFrame;
    for (const word of scene.text.trim().split(/\s+/)) {
      const clip = clips[clipIndex++];
      // Identify audible samples using a small fraction of the word's peak.
      let peak = 0;
      for (let i = 0; i < clip.data.length; i += 2) peak = Math.max(peak, Math.abs(clip.data.readInt16LE(i)));
      if (!peak) throw new Error(`Piper generated silent audio for ${word}`);
      const threshold = Math.max(8, Math.floor(peak * 0.005));
      let first = 0, last = clip.data.length / 2 - 1;
      while (first < last && Math.abs(clip.data.readInt16LE(first * 2)) < threshold) first++;
      while (last > first && Math.abs(clip.data.readInt16LE(last * 2)) < threshold) last--;
      // Trim only leading/trailing silence and place the word on frame boundaries.
      const pcm = clip.data.subarray(first * 2, (last + 1) * 2);
      const clipSamples = pcm.length / 2;
      const startFrame = Math.ceil(pos / samplesPerFrame);
      const endFrame = Math.ceil((pos + clipSamples) / samplesPerFrame);
      if (endFrame > scene.endFrame || endFrame <= startFrame) throw new Error(`Narration for ${scene.scene} exceeds its allotted scene duration.`);
      pcm.copy(audio, pos * 2);
      cues.push({ word, startFrame, endFrame, scene: scene.scene });
      pos = (endFrame + 3) * samplesPerFrame;
    }
    console.log(`${scene.scene}: ${scene.text}`);
  }
  const output = path.join(root, 'public', 'agent-engine');
  mkdirSync(output, { recursive: true });
  writeFileSync(path.join(output, 'voiceover.wav'), encodeWav(audio, sampleRate));
  writeFileSync(path.join(output, 'word-cues.json'), JSON.stringify(cues, null, 2) + '\n');
  console.log(`Wrote ${cues.length} measured word cues and ${durationFrames / fps}s of audio to ${output}`);
} finally {
  rmSync(temp, { recursive: true, force: true });
}

function readWav(file) {
  const buffer = readFileSync(file);
  if (buffer.toString('ascii', 0, 4) !== 'RIFF' || buffer.toString('ascii', 8, 12) !== 'WAVE') throw new Error(`Not a WAV: ${file}`);
  let fmt, data;
  for (let p = 12; p + 8 <= buffer.length;) {
    const name = buffer.toString('ascii', p, p + 4), size = buffer.readUInt32LE(p + 4);
    if (p + 8 + size > buffer.length) throw new Error(`Invalid WAV chunk: ${file}`);
    if (name === 'fmt ') fmt = buffer.subarray(p + 8, p + 8 + size);
    if (name === 'data') data = buffer.subarray(p + 8, p + 8 + size);
    p += 8 + size + (size % 2);
  }
  if (!fmt || !data || fmt.readUInt16LE(0) !== 1 || fmt.readUInt16LE(2) !== 1 || fmt.readUInt16LE(14) !== 16) throw new Error(`Expected mono 16-bit PCM WAV: ${file}`);
  return { sampleRate: fmt.readUInt32LE(4), data };
}
function encodeWav(data, sampleRate) {
  const header = Buffer.alloc(44);
  header.write('RIFF', 0); header.writeUInt32LE(36 + data.length, 4); header.write('WAVEfmt ', 8);
  header.writeUInt32LE(16, 16); header.writeUInt16LE(1, 20); header.writeUInt16LE(1, 22);
  header.writeUInt32LE(sampleRate, 24); header.writeUInt32LE(sampleRate * 2, 28);
  header.writeUInt16LE(2, 32); header.writeUInt16LE(16, 34); header.write('data', 36); header.writeUInt32LE(data.length, 40);
  return Buffer.concat([header, data]);
}
