#!/usr/bin/env python3
"""Test the v1 profile, example renderer and deliberately scoped QA utilities."""
import copy
import json
import math
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/'code-video'
sys.path.insert(0,str(ROOT/'tools'))
import vector_profile as vp
import qa
import measured_checks as mc

EXAMPLE=ROOT/'examples/vector-example.json'

class SchemaAndTiming(unittest.TestCase):
    def setUp(self): self.m=vp.load(EXAMPLE)
    def errors(self): return vp.validate(self.m,EXAMPLE.parent)
    def test_schema_itself_is_valid(self):
        vp.Draft202012Validator.check_schema(vp.SCHEMA)
    def test_example_valid_but_explicitly_proposed(self):
        self.assertEqual(self.errors(),[]);self.assertEqual(self.m['purpose'],'illustrative')
    def test_unapproved_production_is_rejected(self):
        self.m['purpose']='production';self.assertTrue(any('CONFIRMED' in e for e in self.errors()))
    def test_approved_production_and_provenance(self):
        self.m['purpose']='production'
        for k in ('fps','duration_seconds'):
            self.m['timing'][k]['status']='CONFIRMED';self.m['timing'][k]['provenance']='user-approved brief'
        self.assertEqual(self.errors(),[])
    def test_duplicate_json_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d,'duplicate.json');p.write_text('{"x":1,"x":2}')
            with self.assertRaisesRegex(ValueError,'duplicate JSON key'): vp.load(p)
    def test_missing_provenance_rejected(self):
        del self.m['timing']['fps']['provenance'];self.assertTrue(self.errors())
    def test_wrong_frame_count_rejected(self):
        self.m['timing']['total_frames']=9;self.assertTrue(any('total_frames' in e for e in self.errors()))
    def test_scene_gap_and_duplicate_id_rejected(self):
        self.m['scenes'][1]['start']=5;self.m['scenes'][1]['id']='intro'
        errors=' '.join(self.errors());self.assertIn('cover timeline',errors);self.assertIn('duplicate scene',errors)
    def test_visibility_end_and_motion_overlap_rejected(self):
        self.m['objects'][-1]['visible'][1]=9
        self.assertTrue(any('invalid visibility' in e for e in self.errors()))
        self.m['objects'][-1]['visible'][1]=8
        self.m['objects'][-1]['animations'].append({'property':'translate_x','start':3,'end':7,'from':0,'to':5,'easing':'linear'})
        self.assertTrue(any('overlapping animation' in e for e in self.errors()))
    def test_unknown_version_or_primitive_rejected(self):
        self.m['schema_version']='2.0.0';self.assertTrue(self.errors())
        self.m=vp.load(EXAMPLE);self.m['objects'][0]['type']='shader';self.assertTrue(self.errors())
    def test_font_asset_missing_and_path_traversal_rejected(self):
        self.m['asset_policy']={'allowed':['font'],'assets':[{'id':'font','kind':'font','path':'../bad.ttf','sha256':'0'*64}]}
        self.assertTrue(any('unsafe asset' in e for e in self.errors()))
    def test_hash_and_asset_scope(self):
        import hashlib
        with tempfile.TemporaryDirectory() as d:
            Path(d,'font.ttf').write_bytes(b'example')
            self.m['asset_policy']={'allowed':['font'],'assets':[{'id':'font','kind':'font','path':'font.ttf','sha256':hashlib.sha256(b'example').hexdigest()}]}
            self.assertEqual(vp.validate(self.m,d),[])
            Path(d,'font.ttf').write_bytes(b'changed')
            self.assertTrue(any('hash mismatch' in e for e in vp.validate(self.m,d)))

class RendererTests(unittest.TestCase):
    def setUp(self): self.m=vp.load(EXAMPLE)
    def test_golden_outputs_exact_svg_bytes(self):
        for f in (0,7):
            actual=vp.render(self.m,f,EXAMPLE.parent);ET.fromstring(actual)
            self.assertEqual(actual,(ROOT/f'examples/frame-{f}.svg').read_bytes())
    def test_seek_order_independent(self):
        order=[7,0,4,7,4,0];got=[vp.render(self.m,f,EXAMPLE.parent) for f in order]
        self.assertEqual(got[0],got[3]);self.assertEqual(got[1],got[5]);self.assertEqual(got[2],got[4])
    def test_smoothstep_and_inclusive_animation_endpoint(self):
        token=self.m['objects'][-1]
        self.assertEqual(vp.values(token,0)['translate_x'],0)
        self.assertAlmostEqual(vp.values(token,4)['translate_x'],100*208/343)
        self.assertEqual(vp.values(token,7)['translate_x'],100)
    def test_intervals_are_end_exclusive_and_frame_zero_based(self):
        self.m['objects'][-1]['visible']=[1,7]
        self.assertNotIn(b'id="token"',vp.render(self.m,0,EXAMPLE.parent))
        self.assertNotIn(b'id="token"',vp.render(self.m,7,EXAMPLE.parent))
        with self.assertRaises(ValueError): vp.render(self.m,8,EXAMPLE.parent)
    def test_camera_and_screen_space_bounds(self):
        self.m['camera']={'anchor':[80,45],'offset':[10,0],'scale':2}
        world=qa.box_at(self.m['objects'][-1],0,self.m['camera'])
        screen=qa.box_at(self.m['objects'][1],0,self.m['camera'])
        self.assertEqual(world,[-26.0,29.0,6.0,61.0])
        self.assertEqual(screen,[9.0,9.0,151.0,81.0])
    def test_embedded_declared_font_and_escaped_text(self):
        # Synthetic bytes test data flow only; they are not a valid font or text-metrics evidence.
        import hashlib
        with tempfile.TemporaryDirectory() as d:
            font=b'synthetic font bytes';Path(d,'font.ttf').write_bytes(font)
            self.m['asset_policy']={'allowed':['font'],'assets':[{'id':'fontA','kind':'font','path':'font.ttf','sha256':hashlib.sha256(font).hexdigest()}]}
            self.m['objects'].append({'id':'textA','type':'text','visible':[0,8],'space':'screen','z':3,
                'geometry':{'x':10,'y':20,'text':'foreign & central banks < C','font_asset':'fontA','font_size':8},
                'style':{'fill':'#FFFFFF','stroke':None,'stroke_width':0,'opacity':1},'animations':[]})
            self.assertEqual(vp.validate(self.m,d),[])
            svg=vp.render(self.m,0,d); ET.fromstring(svg)
            self.assertIn(b'data:font/ttf;base64,',svg)
            self.assertIn(b'foreign &amp; central banks &lt; C',svg)
            self.assertEqual(qa.report(self.m,d)['analytic_shape_canvas_bounds']['status'],'PARTIAL')
            self.m['objects'][-1]['geometry']['text']='two\nlines'
            self.assertTrue(vp.validate(self.m,d))
            self.m['objects'][-1]['geometry']['text']='bad\x00xml'
            self.assertTrue(any('invalid XML' in e for e in vp.validate(self.m,d)))
    def test_checked_in_example_hashes_match_actual_bytes(self):
        import hashlib
        for line in (ROOT/'examples/SHA256SUMS').read_text().splitlines():
            digest,filename=line.split('  ',1)
            self.assertEqual(digest,hashlib.sha256((ROOT/'examples'/filename).read_bytes()).hexdigest())
    def test_actual_fixture_qa_scopes(self):
        r=qa.report(self.m,EXAMPLE.parent)
        self.assertEqual(r['overall'],'PARTIAL')
        self.assertEqual(r['analytic_shape_canvas_bounds']['status'],'PASS')
        self.assertEqual(r['all_frame_seekability']['status'],'PARTIAL')
        self.assertEqual(r['raster_playback_audio_platform_accessibility']['status'],'NOT CHECKED')
    def test_qa_detects_actual_out_of_bounds(self):
        self.m['objects'][-1]['geometry']['cx']=-4
        self.assertEqual(qa.report(self.m,EXAMPLE.parent)['overall'],'FAIL')

class MeasurementTests(unittest.TestCase):
    def setUp(self): self.p=json.loads((ROOT/'examples/measurements-example.json').read_text())
    def get(self,id): return next(x for x in self.p['checks'] if x['id']==id)
    def test_synthetic_examples_are_only_partial_broader_review(self):
        r=mc.report(self.p);self.assertEqual(r['broader_render_review'],'PARTIAL')
        self.assertTrue(all(x['status']=='PASS' for x in r['results']))
    def test_bounds_failure(self):
        self.get('viewport-box')['inner'][2]=161;self.assertEqual(mc.report(self.p)['broader_render_review'],'FAIL')
    def test_text_overlap_failure(self):
        self.get('two-labels')['b']=[35,10,80,20];self.assertEqual(mc.run(self.get('two-labels'))['status'],'FAIL')
    def test_rect_containment_failure(self):
        self.get('inside-panel')['inner']=[1,1,99,49];self.assertEqual(mc.run(self.get('inside-panel'))['status'],'FAIL')
    def test_circle_corner_failure(self):
        self.get('inside-circle')['inner']=[25,25,75,75];self.assertEqual(mc.run(self.get('inside-circle'))['status'],'FAIL')
    def test_connector_miss_failure(self):
        self.get('connector-contact')['endpoint']=[83,50];self.assertEqual(mc.run(self.get('connector-contact'))['status'],'FAIL')
    def test_contrast_checks_unrounded_srgb(self):
        self.assertAlmostEqual(mc.contrast('#FFFFFF','#000000'),21)
        self.get('contrast-white')['foreground']='#747474';self.assertEqual(mc.run(self.get('contrast-white'))['status'],'FAIL')
    def test_caption_width_failure(self):
        self.get('caption-line')['inner']=[10,5,130,25];self.assertEqual(mc.run(self.get('caption-line'))['status'],'FAIL')
    def test_missing_evidence_rejected(self):
        self.p['evidence']='';self.assertRaises(ValueError,mc.report,self.p)
    def test_nonfinite_numbers_rejected(self):
        self.get('inside-circle')['radius']=math.nan;self.assertRaises(ValueError,mc.report,self.p)

if __name__=='__main__': unittest.main(verbosity=2)
