const {test} = require('node:test');
const assert = require('node:assert/strict');
const {buildMusicSegments} = require('../.audio-test-build/AudioTrack.js');

test('music gain is reduced by exactly 8 dB over speech frames', () => {
  const segments = buildMusicSegments(120, [{startFrame: 20, endFrame: 40}, {startFrame: 70, endFrame: 90}], 0.25);
  assert.deepEqual(segments.map(({startFrame,endFrame}) => [startFrame,endFrame]), [[0,20],[20,40],[40,70],[70,90],[90,120]]);
  for (const i of [1,3]) assert.ok(Math.abs(20*Math.log10(segments[i].volume/0.25)+8) < 1e-10);
  for (const i of [0,2,4]) assert.equal(segments[i].volume,0.25);
});

test('overlapping and adjacent ranges remain ducked without a gap', () => {
  const segments = buildMusicSegments(12, [{startFrame:2,endFrame:7},{startFrame:5,endFrame:10},{startFrame:10,endFrame:11}],0.5);
  assert.equal(segments[0].volume,0.5);
  for (const segment of segments.filter(s => s.startFrame >= 2 && s.startFrame < 11)) {
    assert.ok(Math.abs(20*Math.log10(segment.volume/0.5)+8) < 1e-10);
  }
  assert.equal(segments.at(-1).startFrame,11);
  assert.equal(segments.at(-1).volume,0.5);
});

test('prototype AudioTrack renders silently with no timing props or audio assets', () => {
  const React = require('react');
  const {renderToStaticMarkup} = require('react-dom/server');
  const {AudioTrack} = require('../.audio-test-build/AudioTrack.js');
  assert.equal(renderToStaticMarkup(React.createElement(AudioTrack)), '');
});
