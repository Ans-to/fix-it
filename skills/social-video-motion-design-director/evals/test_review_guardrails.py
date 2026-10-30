#!/usr/bin/env python3
"""Mechanical examples for review guardrails, not a test of an AI agent's judgment."""
import hashlib
import json
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def hash_and_bytes_match(file_bytes, declared_sha256, embedded_bytes):
    """Caller must supply the actual shipped file bytes and decoded embedded bytes."""
    return (hashlib.sha256(file_bytes).hexdigest() == declared_sha256
            and file_bytes == embedded_bytes)


def semantic_json_equal(file_bytes, embedded_bytes):
    return json.loads(file_bytes) == json.loads(embedded_bytes)


def gap(center1, r1, center2, r2):
    return math.dist(center1, center2) - r1 - r2


def touches(center1, r1, center2, r2, tolerance):
    return abs(gap(center1, r1, center2, r2)) <= tolerance


def box_fits_circle(box, center, radius, margin=0):
    """Conservative circle containment; a box may fail even if glyphs visually fit."""
    x0, y0, x1, y1 = box
    usable = radius - margin
    return usable >= 0 and all(math.dist((x, y), center) <= usable
                               for x in (x0, x1) for y in (y0, y1))


def contrast(fg, bg):
    def lum(rgb):
        def lin(v):
            v /= 255
            return v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4
        return .2126*lin(rgb[0]) + .7152*lin(rgb[1]) + .0722*lin(rgb[2])
    a, b = sorted((lum(fg), lum(bg)), reverse=True)
    return (a+.05)/(b+.05)


def blend(fg, bg, alpha):
    return tuple(round(alpha*f + (1-alpha)*b) for f, b in zip(fg, bg))


class ArtifactGuardrails(unittest.TestCase):
    def test_exact_bytes_and_declared_hash_match(self):
        file_bytes = b'{"one": 1}\n'
        sha = hashlib.sha256(file_bytes).hexdigest()
        self.assertTrue(hash_and_bytes_match(file_bytes, sha, file_bytes))

    def test_identical_json_is_not_automatically_identical_bytes(self):
        file_bytes, embedded = b'{"one": 1}\n', b'{"one":1}'
        self.assertTrue(semantic_json_equal(file_bytes, embedded))
        self.assertFalse(hash_and_bytes_match(file_bytes, hashlib.sha256(file_bytes).hexdigest(), embedded))

    def test_wrong_hash_does_not_pass_even_when_bytes_match(self):
        self.assertFalse(hash_and_bytes_match(b'{}\n', '0'*64, b'{}\n'))

    def test_explicit_final_newline_reconstruction(self):
        embedded_content = '{"one": 1}'
        self.assertEqual((embedded_content+'\n').encode(), b'{"one": 1}\n')
        self.assertNotEqual(embedded_content.encode(), b'{"one": 1}\n')


class GeometryGuardrails(unittest.TestCase):
    def test_left_and_right_token_ends_reach_both_nodes(self):
        self.assertTrue(touches((250, 0), 70, (370, 0), 50, 0.1))
        self.assertTrue(touches((830, 0), 70, (710, 0), 50, 0.1))

    def test_central_movement_alone_does_not_prove_contact(self):
        self.assertFalse(touches((250, 0), 70, (380, 0), 50, 0.1))
        self.assertEqual(gap((250, 0),70,(380, 0),50),10)
        self.assertFalse(touches((830, 0), 70, (700, 0), 50, 0.1))

    def test_center_inside_node_is_overlap_not_edge_contact(self):
        self.assertLess(gap((250,0),70,(320,0),50),0)
        self.assertFalse(touches((250,0),70,(320,0),50,0.1))

    def test_box_fully_inside_circle(self):
        self.assertTrue(box_fits_circle((-10,-10,10,10),(0,0),30,margin=2))

    def test_box_looks_within_bounding_square_but_not_inside_circle(self):
        self.assertFalse(box_fits_circle((-25,-25,25,25),(0,0),30))


class ContrastGuardrails(unittest.TestCase):
    def test_each_used_pair_must_be_checked_individually(self):
        night=(16,27,43); surface=(28,45,64); ivory=(247,244,236); gold=(234,199,119)
        ratios={name:contrast(fg,bg) for name,fg,bg in [
            ('ivory/night',ivory,night),('gold/night',gold,night),
            ('ivory/surface',ivory,surface),('gold/surface',gold,surface)]}
        self.assertEqual(len(ratios),4)
        self.assertTrue(all(value>4.5 for value in ratios.values()))

    def test_faded_text_has_different_effective_contrast(self):
        fg=(247,244,236); bg=(16,27,43)
        self.assertLess(contrast(blend(fg,bg,.2),bg),contrast(fg,bg))


class SkillPackageGuardrails(unittest.TestCase):
    def test_skill_reference_exists_and_is_wired(self):
        skill=(ROOT/'SKILL.md').read_text()
        ref=ROOT/'references/visual-proof-and-handoff.md'
        self.assertIn('references/visual-proof-and-handoff.md',skill)
        self.assertTrue(ref.is_file())

    def test_reference_covers_required_quality_categories(self):
        ref=(ROOT/'references/visual-proof-and-handoff.md').read_text().lower()
        for phrase in ('shipped bytes', 'listening-only', 'foreign central banks', 'network effect',
                       'edge-to-edge gap', 'bookend', 'every distinct foreground',
                       'circles', 'before and after'):
            with self.subTest(phrase=phrase): self.assertIn(phrase,ref)

if __name__ == '__main__': unittest.main(verbosity=2)
