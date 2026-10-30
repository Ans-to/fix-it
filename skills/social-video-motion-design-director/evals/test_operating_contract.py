#!/usr/bin/env python3
"""Examples of operational contract checks. Not an AI-agent behavioral benchmark."""
import datetime
import hashlib
import math
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def review_status(checked, total, failures=0):
    if failures: return 'FAIL'
    if total <= 0 or checked < 0 or checked > total: raise ValueError('invalid scope')
    if checked == 0: return 'NOT CHECKED'
    return 'PASS' if checked == total else 'PARTIAL'


def locked_frame_count(seconds, fps, duration_confirmed, fps_confirmed):
    if not duration_confirmed or not fps_confirmed: return None
    value = Fraction(seconds) * Fraction(fps)
    return (2*value.numerator + value.denominator) // (2*value.denominator)


def extract_lf_fenced_bytes(markdown):
    opener = b'```json\n'
    start = markdown.index(opener) + len(opener)
    end = markdown.index(b'```\n', start)
    if end == start or markdown[end-1:end] != b'\n': raise ValueError('closing fence not on its own line')
    return markdown[start:end]


def verify_manifest(file_bytes, markdown, declared_sha):
    embedded = extract_lf_fenced_bytes(markdown)
    return (hashlib.sha256(file_bytes).hexdigest() == declared_sha
            and hashlib.sha256(embedded).hexdigest() == declared_sha
            and file_bytes == embedded)


def literal_qualifier_present(qualifier, wording):
    # Literal audit only: absence does not prove a semantic contradiction.
    return qualifier.casefold() in wording.casefold()


def reading_estimate_seconds(text):
    return max(1.5, len(text)/15)


def line_fits(text, width, measure):
    return measure(text) <= width


def sampling_frames(scenes, events, cues, total):
    """Events are (start,settle) frame points; scene and cue ranges are half-open."""
    out = set()
    def add(f):
        if 0 <= f < total: out.add(f)
    for a,b in scenes:
        add(a);add((a+b-1)//2);add(b-1)
        add(a-1);add(a)  # both sides of scene start
    for a,b in events:
        add(a);add((a+b)//2);add(b)
    for a,b in cues:
        for f in (a-1,a,b-1,b): add(f)
    return out


def source_is_recent(access_date, today, days=30):
    delta = (today-access_date).days
    return 0 <= delta <= days


def revision_verified(before, after, recheck):
    return bool(before and after and recheck)


class ReviewScopeTests(unittest.TestCase):
    def test_selected_checks_are_partial_for_wider_scope(self):
        self.assertEqual(review_status(3,100),'PARTIAL')
    def test_exact_checked_subscope_can_pass(self):
        self.assertEqual(review_status(3,3),'PASS')
    def test_no_evidence_is_not_checked(self):
        self.assertEqual(review_status(0,10),'NOT CHECKED')
    def test_observed_failure_wins(self):
        self.assertEqual(review_status(2,10,1),'FAIL')
    def test_invalid_counts_rejected(self):
        with self.assertRaises(ValueError): review_status(11,10)


class TimingTests(unittest.TestCase):
    def test_assumed_fps_cannot_produce_locked_frame_count(self):
        self.assertIsNone(locked_frame_count(60,30,True,False))
    def test_approved_30fps_and_duration(self):
        self.assertEqual(locked_frame_count(60,30,True,True),1800)
    def test_fractional_fps_is_rational_and_rounding_explicit(self):
        self.assertEqual(locked_frame_count(60,Fraction(30000,1001),True,True),1798)


class IntegrityTests(unittest.TestCase):
    def test_actual_file_and_exact_embedded_lf_bytes(self):
        data=b'{"a": 1}\n'; doc=b'heading\n```json\n'+data+b'```\n';sha=hashlib.sha256(data).hexdigest()
        self.assertTrue(verify_manifest(data,doc,sha))
    def test_semantic_match_is_not_byte_match(self):
        data=b'{"a": 1}\n'; doc=b'```json\n{"a":1}\n```\n';sha=hashlib.sha256(data).hexdigest()
        self.assertFalse(verify_manifest(data,doc,sha))
    def test_missing_file_final_newline_is_not_silently_repaired(self):
        data=b'{"a":1}';doc=b'```json\n{"a":1}\n```\n';sha=hashlib.sha256(data).hexdigest()
        self.assertFalse(verify_manifest(data,doc,sha))
    def test_wrong_hash_fails(self):
        data=b'{}\n';self.assertFalse(verify_manifest(data,b'```json\n{}\n```\n','0'*64))


class CaptionAndQualifierTests(unittest.TestCase):
    def test_removed_foreign_qualifier_is_flagged_for_review(self):
        self.assertTrue(literal_qualifier_present('foreign','foreign central banks'))
        self.assertFalse(literal_qualifier_present('foreign','for central banks'))
    def test_short_reading_hold_uses_heuristic_floor(self):
        self.assertEqual(reading_estimate_seconds('hello'),1.5)
    def test_longer_reading_hold_accounts_for_characters(self):
        self.assertEqual(reading_estimate_seconds('a'*45),3.0)
    def test_character_count_is_not_glyph_width(self):
        # Synthetic glyph widths show why the same character count is insufficient.
        measure=lambda s: sum(3 if x=='W' else 1 for x in s)
        self.assertTrue(line_fits('iiii',8,measure))
        self.assertFalse(line_fits('WWWW',8,measure))


class GeometryAndContrastTests(unittest.TestCase):
    def test_connector_contact_tolerance_scales_with_short_side(self):
        tolerance = max(1, 2*min(1080,1920)/1080)
        def contact(gap): return abs(gap) <= tolerance
        self.assertTrue(contact(2))
        self.assertFalse(contact(2.01))
        self.assertFalse(contact(-50))  # deep overlap is not edge contact
    def test_each_corner_of_rectangle_fits_circle_with_margin(self):
        def inside(box, radius, margin):
            x0,y0,x1,y1=box
            return all(math.hypot(x,y) <= radius-margin for x in (x0,x1) for y in (y0,y1))
        self.assertTrue(inside((-3,-3,3,3),10,1))
        self.assertFalse(inside((-8,-8,8,8),10,1))
    def test_contrast_threshold_is_compared_without_rounding(self):
        self.assertFalse(4.499 >= 4.5)
        self.assertTrue(4.5 >= 4.5)


class SamplingAndRevisionTests(unittest.TestCase):
    def test_cut_entry_and_caption_boundaries_are_included(self):
        s=sampling_frames([(0,10),(10,20)],[(3,7)],[(0,6),(6,20)],20)
        self.assertTrue({0,4,9,10,14,19,3,5,7,5,6} <= s)
        self.assertTrue(all(0<=f<20 for f in s))
    def test_inaccessible_or_stale_source_is_not_recent(self):
        now=datetime.date(2026,10,30)
        self.assertTrue(source_is_recent(datetime.date(2026,10,1),now))
        self.assertFalse(source_is_recent(datetime.date(2026,9,1),now))
    def test_missing_before_or_after_does_not_verify_fix(self):
        self.assertFalse(revision_verified(None,'after.png','rechecked'))
        self.assertFalse(revision_verified('before.png',None,'rechecked'))
        self.assertTrue(revision_verified('before.png','after.png','rechecked'))


class SkillPackagingTests(unittest.TestCase):
    def test_all_required_companions_exist(self):
        for file in ['references/operating-contract.md','references/creative-direction.md',
                     'references/production-and-review.md','references/visual-proof-and-handoff.md',
                     'references/platform-sources.md','templates/production-plan.md',
                     'templates/claim-proof-map.md','templates/review.md','templates/revision-log.md']:
            with self.subTest(file=file): self.assertTrue((ROOT/file).is_file())
    def test_standalone_fallback_and_routing_documented(self):
        skill=(ROOT/'SKILL.md').read_text()
        for phrase in ['Fallback minimum','Script-only','PARTIAL','PROPOSED','NOT CHECKED']:
            with self.subTest(phrase=phrase): self.assertIn(phrase,skill)

if __name__=='__main__': unittest.main(verbosity=2)
