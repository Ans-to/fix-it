#!/usr/bin/env python3
"""Mechanical checks for a synthetic director handoff; not a semantic evaluator."""
import copy
import json
import unittest
from pathlib import Path

PLAN = Path(__file__).parent / 'fixtures' / 'queue-plan.json'


def at(obj, frame):
    if not obj['visible'][0] <= frame < obj['visible'][1]:
        return None
    points = obj['keyframes']
    if frame <= points[0][0]:
        return points[0][1], points[0][2]
    for a, b in zip(points, points[1:]):
        if frame <= b[0]:
            t = (frame - a[0]) / (b[0] - a[0])
            return a[1] + t * (b[1] - a[1]), a[2] + t * (b[2] - a[2])
    return points[-1][1], points[-1][2]


def intersect(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def timeline_valid(p):
    cursor = 0
    for s in p['segments']:
        if not isinstance(s['start'], int) or not isinstance(s['end'], int): return False
        if s['start'] != cursor or s['end'] <= s['start']: return False
        cursor = s['end']
    return cursor == p['canvas']['total_frames']


def validate_keyframes(p):
    total = p['canvas']['total_frames']
    for obj in p['objects']:
        begin, end = obj['visible']
        points = obj['keyframes']
        if not (0 <= begin < end <= total) or not points: return False
        if points[0][0] != begin or points[-1][0] != end-1: return False
        if any(b[0] <= a[0] for a, b in zip(points, points[1:])): return False
    return True


def collisions(p):
    found = []
    for f in range(p['canvas']['total_frames']):
        for obj in p['objects']:
            pos = at(obj, f)
            if pos is None: continue
            x, y = pos; r = obj['radius']; box = (x-r,y-r,x+r,y+r)
            for label in p['protected_labels']:
                if label['visible'][0] <= f < label['visible'][1] and intersect(box,label['box']):
                    found.append((f,obj['id'],label['id']))
    return found


def within_margin(p):
    w, h, m = p['canvas']['width'], p['canvas']['height'], p['safe_margin']
    for f in range(p['canvas']['total_frames']):
        for obj in p['objects']:
            pos = at(obj, f)
            if pos is None: continue
            x,y=pos; r=obj['radius']
            if x-r < m or x+r > w-m or y-r < m or y+r > h-m: return False
    return all(m <= b[0] < b[2] <= w-m and m <= b[1] < b[3] <= h-m
               for b in (label['box'] for label in p['protected_labels']))


def facts_valid(p):
    for fact in p['facts']:
        if fact['status'] not in ('confirmed', 'illustrative', 'unverified'): return False
        if fact['status'] == 'confirmed' and not fact.get('source'): return False
    return True


def review_valid(p):
    # Minimal fixture schema; this does not establish that scope is complete.
    states = {'PASS', 'PARTIAL', 'FAIL', 'NOT CHECKED', 'NEEDS HUMAN REVIEW', 'NOT APPLICABLE'}
    return all(item['status'] in states
               and (item['status'] not in {'PASS', 'PARTIAL', 'FAIL'} or bool(item.get('evidence')))
               and (item['status'] != 'NOT APPLICABLE' or bool(item.get('reason')))
               for item in p['review'])


class ContractTests(unittest.TestCase):
    def setUp(self): self.p = json.loads(PLAN.read_text())
    def test_timeline_covers_exact_frame_count(self): self.assertTrue(timeline_valid(self.p))
    def test_bad_gap_is_detected(self):
        self.p['segments'][1]['start'] += 1
        self.assertFalse(timeline_valid(self.p))
    def test_bad_overlap_is_detected(self):
        self.p['segments'][1]['start'] -= 1
        self.assertFalse(timeline_valid(self.p))
    def test_end_inclusive_91_frame_mistake_is_detected(self):
        self.p['segments'][-1]['end'] += 1
        self.assertFalse(timeline_valid(self.p))
    def test_keyframes_are_well_formed(self): self.assertTrue(validate_keyframes(self.p))
    def test_duplicate_keyframe_is_detected(self):
        self.p['objects'][0]['keyframes'][1][0] = 0
        self.assertFalse(validate_keyframes(self.p))
    def test_no_planned_label_circle_collisions(self): self.assertEqual(collisions(self.p), [])
    def test_original_label_position_collision_detected(self):
        self.p['protected_labels'][0]['box'] = [150,250,210,275]
        hits = collisions(self.p)
        # The original position now collides during the revised arrival motion.
        self.assertTrue(any(18 <= frame <= 33 for frame, _, _ in hits), hits)
    def test_bad_repair_collision_detected(self):
        self.p['protected_labels'][0]['box'] = [150,375,210,390]
        self.assertTrue(any(120 <= frame < 150 for frame, _, _ in collisions(self.p)))
    def test_project_margin(self): self.assertTrue(within_margin(self.p))
    def test_out_of_bounds_is_detected(self):
        self.p['objects'][0]['keyframes'][0][1] = 10
        self.assertFalse(within_margin(self.p))
    def test_arrival_order_is_explicit(self):
        objs=self.p['objects']; self.assertEqual([o['id'] for o in objs], ['R1','R2','R3'])
        self.assertLess(objs[0]['visible'][0], objs[1]['visible'][0])
        self.assertLess(objs[1]['visible'][0], objs[2]['visible'][0])
        # The first item visibly reaches its position before the next appears.
        self.assertLess(objs[0]['keyframes'][1][0], objs[1]['visible'][0])
        self.assertLess(objs[1]['keyframes'][1][0], objs[2]['visible'][0])
    def test_first_out_in_planned_coordinates(self):
        by_id={o['id']: o for o in self.p['objects']}
        self.assertEqual(at(by_id['R1'], 149), (180,470))
        self.assertEqual(at(by_id['R2'], 149), (180,320))
        self.assertEqual(at(by_id['R3'], 149), (260,320))
    def test_claims_are_labeled(self): self.assertTrue(facts_valid(self.p))
    def test_unverified_source_cannot_be_confirmed(self):
        self.p['facts'].append({'claim':'40% increase','status':'confirmed','source':None})
        self.assertFalse(facts_valid(self.p))
    def test_review_statuses_need_evidence_for_pass(self): self.assertTrue(review_valid(self.p))
    def test_unsubstantiated_pass_is_detected(self):
        self.p['review'].append({'check':'audio reviewed','status':'PASS','evidence':None})
        self.assertFalse(review_valid(self.p))
    def test_partial_requires_some_evidence(self):
        item={'check':'full geometry','status':'PARTIAL','evidence':'three selected frames'}
        self.p['review'].append(item)
        self.assertTrue(review_valid(self.p))
        item['evidence']=None
        self.assertFalse(review_valid(self.p))
    def test_not_applicable_requires_reason(self):
        item={'check':'audio','status':'NOT APPLICABLE','reason':'intentionally silent'}
        self.p['review'].append(item)
        self.assertTrue(review_valid(self.p))
        item['reason']=''
        self.assertFalse(review_valid(self.p))

if __name__ == '__main__': unittest.main(verbosity=2)
