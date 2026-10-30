import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import { existsSync, mkdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const output = path.join(root, 'out', 'video.mp4');
const voiceover = path.join(root, 'public', 'agent-engine', 'voiceover.wav');
const inputProps = { hasVoiceover: existsSync(voiceover) };
const browserExecutable = process.env.REMOTION_BROWSER_EXECUTABLE || undefined;

async function main() {
  mkdirSync(path.dirname(output), { recursive: true });
  if (!inputProps.hasVoiceover) {
    console.warn('Warning: public/agent-engine/voiceover.wav is missing; the render will be silent.');
  }
  console.log('Bundling composition...');
  let lastBundleProgress = -1;
  const serveUrl = await bundle({
    entryPoint: path.join(root, 'src', 'index.ts'),
    rootDir: root,
    webpackOverride: (config) => ({
      ...config,
      resolve: {
        ...config.resolve,
        extensionAlias: { ...config.resolve?.extensionAlias, '.js': ['.ts', '.tsx', '.js'], '.jsx': ['.tsx', '.jsx'] },
      },
    }),
    onProgress: (progress) => {
      const percent = Math.floor(progress / 10) * 10;
      if (percent !== lastBundleProgress) {
        lastBundleProgress = percent;
        console.log(`Bundle: ${percent}%`);
      }
    },
  });
  const composition = await selectComposition({
    serveUrl,
    id: 'main-composition',
    inputProps,
    browserExecutable,
  });
  const frames = composition.durationInFrames;
  console.log(`Rendering full composition (${frames} frames at ${composition.fps} fps) to ${output}`);
  let lastRenderProgress = -1;
  await renderMedia({
    composition,
    serveUrl,
    inputProps,
    browserExecutable,
    codec: 'h264',
    outputLocation: output,
    concurrency: 2,
    onProgress: ({ progress, renderedFrames, encodedFrames }) => {
      const percent = Math.floor(progress * 100);
      if (percent >= lastRenderProgress + 5 || percent === 100 && lastRenderProgress !== 100) {
        lastRenderProgress = percent;
        console.log(`Render: ${percent}% (${renderedFrames} rendered, ${encodedFrames} encoded)`);
      }
    },
  });
  if (!existsSync(output) || statSync(output).size === 0) throw new Error('Render completed without a nonempty output file.');
  console.log(`Finished: ${output} (${statSync(output).size} bytes)`);
}

main().catch((error) => {
  console.error('Render failed:', error);
  process.exitCode = 1;
});
