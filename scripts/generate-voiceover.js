/**
 * Assemble natural scene recordings and forced-align words to the audio.
 * Default: re-align recordings in public/agent-engine/scenes.
 * Set ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID to synthesize fresh scenes.
 */
import { spawnSync } from 'node:child_process';
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync, mkdirSync, copyFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const output = path.join(root, 'public', 'agent-engine');
const sourceDir = process.env.VOICE_SCENES_DIR || path.join(output, 'scenes');
const scenes = JSON.parse(readFileSync(path.join(root, 'scripts/narration.json'), 'utf8'));
const fps = 30, durationFrames = 1547, sampleRate = 24000, samplesPerFrame = sampleRate / fps;
const python = process.env.ALIGN_PYTHON || 'python3';
const bundledFfmpeg = path.join(root, 'node_modules', '@remotion', `compositor-${process.platform}-${process.arch}-gnu`, 'ffmpeg');
const ffmpeg = process.env.FFMPEG_PATH || (existsSync(bundledFfmpeg) ? bundledFfmpeg : 'ffmpeg');
const sceneFiles = ['hook', 'twist', 'shift', 'mechanism', 'payoff', 'outro'];
const apiKey = process.env.ELEVENLABS_API_KEY;
const voiceId = process.env.ELEVENLABS_VOICE_ID;
if (apiKey && !voiceId) throw new Error('Set ELEVENLABS_VOICE_ID along with ELEVENLABS_API_KEY.');
if (scenes.length !== sceneFiles.length) throw new Error('Expected six scene definitions.');

const temp = mkdtempSync(path.join(os.tmpdir(), 'agent-voiceover-'));
try {
  const audio = Buffer.alloc(durationFrames * samplesPerFrame * 2);
  const cues = [];
  const stagedClips = [];
  for (let index = 0; index < scenes.length; index++) {
    const scene = scenes[index];
    const input = path.join(temp, `${sceneFiles[index]}-input.wav`);
    if (apiKey) {
      const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${encodeURIComponent(voiceId)}/with-timestamps?output_format=pcm_24000`, {
        method: 'POST',
        headers: { 'xi-api-key': apiKey, 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: `${scene.text}.`, model_id: process.env.ELEVENLABS_MODEL_ID || 'eleven_multilingual_v2' }),
      });
      if (!response.ok) throw new Error(`ElevenLabs request for ${scene.scene} failed (HTTP ${response.status}).`);
      const result = await response.json();
      if (!result.audio_base64) throw new Error(`ElevenLabs returned no audio for ${scene.scene}.`);
      writeFileSync(input, encodeWav(Buffer.from(result.audio_base64, 'base64'), sampleRate));
    } else {
      const source = path.join(sourceDir, `${sceneFiles[index]}.wav`);
      if (!existsSync(source)) throw new Error(`Missing recording ${source}. Provide six scene WAVs or configure ElevenLabs.`);
      copyFileSync(source, input);
    }
    const normalized = path.join(temp, `${sceneFiles[index]}.wav`);
    const aligned = path.join(temp, `${sceneFiles[index]}-16k.wav`);
    convert(input, normalized, sampleRate);
    convert(input, aligned, 16000);
    const clip = readWav(normalized);
    if (clip.sampleRate !== sampleRate) throw new Error('Unexpected normalized sample rate.');
    const position = (scene.startFrame + 9) * samplesPerFrame;
    const clipSamples = clip.data.length / 2;
    if (position + clipSamples > scene.endFrame * samplesPerFrame) throw new Error(`${scene.scene} recording exceeds its scene duration.`);
    const result = spawnSync(python, [path.join(root, 'scripts', 'align-voiceover.py'), aligned, scene.text], { encoding: 'utf8' });
    if (result.error || result.status !== 0) throw new Error(`Alignment failed for ${scene.scene}: ${result.error || result.stderr}`);
    const segments = JSON.parse(result.stdout);
    const originalWords = scene.text.trim().split(/\s+/);
    if (segments.length !== originalWords.length) throw new Error(`Alignment length mismatch for ${scene.scene}`);
    const sceneCues = segments.map((segment, i) => ({
      word: originalWords[i],
      startFrame: scene.startFrame + 9 + Math.ceil(segment.startSeconds * fps),
      endFrame: scene.startFrame + 9 + Math.ceil(Math.min(segment.endSeconds, clipSamples / sampleRate) * fps),
      scene: scene.scene,
    }));
    for (let i = 0; i < sceneCues.length; i++) {
      const cue = sceneCues[i];
      if (i + 1 < sceneCues.length) cue.endFrame = Math.min(cue.endFrame, sceneCues[i + 1].startFrame);
      if (cue.endFrame <= cue.startFrame || cue.endFrame > scene.endFrame) throw new Error(`Invalid aligned frames for ${cue.word}`);
    }
    clip.data.copy(audio, position * 2);
    cues.push(...sceneCues);
    stagedClips.push([normalized, path.join(output, 'scenes', `${sceneFiles[index]}.wav`)]);
    console.log(`${scene.scene}: ${scene.text} (${(clipSamples / sampleRate).toFixed(2)}s, ${sceneCues.length} aligned words)`);
  }
  mkdirSync(output, { recursive: true });
  if (apiKey) {
    mkdirSync(path.join(output, 'scenes'), { recursive: true });
    for (const [source, dest] of stagedClips) copyFileSync(source, dest);
  }
  writeFileSync(path.join(output, 'voiceover.wav'), encodeWav(audio, sampleRate));
  writeFileSync(path.join(output, 'word-cues.json'), JSON.stringify(cues, null, 2) + '\n');
  console.log(`Wrote ${cues.length} acoustically estimated word cues and ${durationFrames / fps}s of audio.`);
} finally {
  rmSync(temp, { recursive: true, force: true });
}

function convert(input, dest, rate) {
  const result = spawnSync(ffmpeg, ['-v', 'error', '-y', '-i', input, '-ac', '1', '-ar', String(rate), '-c:a', 'pcm_s16le', dest], { encoding: 'utf8' });
  if (result.error || result.status !== 0) throw new Error(`FFmpeg conversion failed: ${result.error || result.stderr}`);
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
function encodeWav(data, rate) {
  const header = Buffer.alloc(44);
  header.write('RIFF', 0); header.writeUInt32LE(36 + data.length, 4); header.write('WAVEfmt ', 8);
  header.writeUInt32LE(16, 16); header.writeUInt16LE(1, 20); header.writeUInt16LE(1, 22);
  header.writeUInt32LE(rate, 24); header.writeUInt32LE(rate * 2, 28);
  header.writeUInt16LE(2, 32); header.writeUInt16LE(16, 34); header.write('data', 36); header.writeUInt32LE(data.length, 40);
  return Buffer.concat([header, data]);
}
