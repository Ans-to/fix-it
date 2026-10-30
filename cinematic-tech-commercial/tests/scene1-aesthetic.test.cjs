const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.join(__dirname, '..');
const read = p => fs.readFileSync(path.join(root, p), 'utf8');

test('scene and preview use only the approved base palette', () => {
  const sources = ['src/scenes/Scene1.tsx', 'src/components/CyberAtmosphere.tsx', 'src/preview.css'];
  const allowed = new Set(['#050507', '#d2ff52', '#ffffff', '#1e2229']);
  for (const file of sources) {
    const source = read(file);
    for (const color of source.match(/#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?\b/g) || []) {
      assert.ok(allowed.has(color.slice(0, 7).toLowerCase()), `${file} uses ${color}`);
    }
    for (const [, channels] of source.matchAll(/rgba?\(\s*(\d+\s*,\s*\d+\s*,\s*\d+)/g)) {
      assert.ok(['210,255,82', '255,255,255'].includes(channels.replace(/\s/g, '')), `${file} uses RGB ${channels}`);
    }
  }
});

test('scene uses HUD terminals, a wireframe token and the palette-safe impact', () => {
  const scene = read('src/scenes/Scene1.tsx');
  assert.match(scene, /<Node name="A"/);
  assert.match(scene, /<Node name="B"/);
  assert.match(scene, /<torusGeometry/);
  assert.match(scene, /text="NEITHER"[^]*?accentMode="lime"/);
  assert.match(scene, /color:LIME/);
  assert.doesNotMatch(scene, /<Marker\b|#173d38|#1f6255|#c9c46b/i);
});
