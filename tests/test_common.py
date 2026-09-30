import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch,MagicMock
import numpy as np
import cv2
from common import frame_ok,save_image,live,demo_frame,panel

class CommonTests(unittest.TestCase):
    def test_invalid_frame(self):
        for f in [None,np.zeros((20,20)),np.zeros((1,20,3),np.uint8)]:
            with self.assertRaises(ValueError):frame_ok(f)
    def test_no_network_camera(self):
        with self.assertRaises(ValueError):live(object(),'https://example.invalid')
    def test_failed_camera_released(self):
        cap=MagicMock();cap.isOpened.return_value=False
        with patch('common.cv2.VideoCapture',return_value=cap):
            with self.assertRaises(ValueError):live(object())
        cap.release.assert_called_once()
    def test_explicit_save_new_unique_files(self):
        f=demo_frame()
        with tempfile.TemporaryDirectory() as d:
            p=save_image(f,d);q=save_image(f,d)
            self.assertNotEqual(p,q);self.assertTrue(np.array_equal(cv2.imread(str(p)),f))
    def test_symlink_save_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'link';p.symlink_to(d,target_is_directory=True)
            with self.assertRaises(ValueError):save_image(demo_frame(),p)
    def test_panel_input_unchanged(self):
        f=demo_frame();a=f.copy();out=panel(f,['hello']);self.assertEqual(out.shape[0],f.shape[0]+90);self.assertTrue(np.array_equal(f,a))

    def test_processing_failure_releases_camera(self):
        cap=MagicMock();cap.isOpened.return_value=True;cap.read.return_value=(True,demo_frame())
        proc=MagicMock();proc.process.side_effect=ValueError('bad frame processing')
        with patch('common.cv2.VideoCapture',return_value=cap),patch('common.cv2.namedWindow'),patch('common.cv2.setMouseCallback'),patch('common.cv2.destroyAllWindows') as cleanup:
            with self.assertRaises(ValueError):live(proc)
        cap.release.assert_called_once();cleanup.assert_called_once()
