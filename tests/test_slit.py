import unittest
import numpy as np
from core import SlitScan
import app
from app import check

class SlitTests(unittest.TestCase):
    def test_release_version(self):
        self.assertEqual(app.__version__, "0.1.0")
    def f(self,v=30):return np.full((20,40,3),v,np.uint8)
    def test_temporal_strips_native(self):check()
    def test_no_input_changes(self):
        f=self.f();s=SlitScan();s.process(f,0);s.process(f,.1);self.assertTrue(np.all(f==30))
    def test_pause(self):
        s=SlitScan();s.process(self.f(),0);s.key(32);s.process(self.f(),.1);self.assertEqual(s.cursor,0)
    def test_horizontal(self):
        s=SlitScan(200);s.key(ord('h'));s.process(self.f(),0);out=s.process(self.f(),.1);self.assertTrue(s.completed);self.assertTrue(np.all(out==30))
    def test_finished_stays(self):
        s=SlitScan(400);s.process(self.f(),0);s.process(self.f(),.1);out=s.process(self.f(90),.2);self.assertTrue(np.all(out==30))
    def test_reset(self):
        s=SlitScan();s.process(self.f(),0);s.key(ord('r'));self.assertIsNone(s.canvas)
    def test_shape_change(self):
        s=SlitScan();s.process(self.f(),0);s.process(np.zeros((50,60,3),np.uint8),.1);self.assertEqual(s.canvas.shape,(50,60,3))
    def test_gap_bounded(self):
        s=SlitScan(120);s.process(self.f(),0);s.process(self.f(),30);self.assertAlmostEqual(s.cursor,12)
    def test_time_reversal(self):
        s=SlitScan();s.process(self.f(),1)
        with self.assertRaises(ValueError):s.process(self.f(),0)
    def test_bad_speed(self):
        with self.assertRaises(ValueError):SlitScan(float('nan'))
