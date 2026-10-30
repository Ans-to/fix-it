const {test} = require('node:test');
const assert = require('node:assert/strict');
const {MOCK_FPS, SCENE_1_DURATION, SCENE_1_TIMINGS} = require('../.mock-test-build/mockTimings.js');

test('mock word cues are ordered and contained in the storyboard-length scene', () => {
  assert.equal(MOCK_FPS, 30);
  assert.equal(SCENE_1_DURATION, 141);
  const frames = Object.values(SCENE_1_TIMINGS);
  assert.ok(frames.every(Number.isInteger));
  assert.ok(frames.every((frame, i) => frame >= 0 && frame < SCENE_1_DURATION && (i === 0 || frame > frames[i-1])));
  assert.equal(SCENE_1_TIMINGS.neither, 86);
});
