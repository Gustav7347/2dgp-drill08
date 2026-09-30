"""과제 채점에 직접 영향을 주는 반복 경계, 좌표, 데이터 검증."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from animation_viewer import (AnimationPlayer, load_atlas, validate_atlas,
                              calculate_scale, frame_geometry, CANVAS_HEIGHT)


class ViewerTests(unittest.TestCase):
    def setUp(self):
        self.data = load_atlas()
        self.animations = self.data['animations']
        self.player = AnimationPlayer(self.animations)

    def test_metadata_and_bonus_requirements(self):
        validate_atlas(self.data)
        counts = [len(a['frames']) for a in self.animations]
        self.assertEqual(counts, [8, 4, 5, 4])
        sizes = {(f['w'], f['h']) for a in self.animations for f in a['frames']}
        self.assertGreater(len(sizes), 1)

    def test_fifth_loop_holds_last_frame_for_full_second(self):
        for index, animation in enumerate(self.animations):
            duration = len(animation['frames']) / animation['fps'] * 5
            self.player.update(duration - .001)
            self.assertFalse(self.player.paused)
            self.assertEqual(self.player.completed_loops, 4)
            self.player.update(.001)
            self.assertTrue(self.player.paused)
            self.assertEqual(self.player.completed_loops, 5)
            self.assertEqual(self.player.frame_index, len(animation['frames'])-1)
            self.player.update(.999)
            self.assertEqual(self.player.animation_index, index)
            self.assertTrue(self.player.paused)
            self.player.update(.001)
            self.assertEqual(self.player.animation_index, (index+1) % 4)
            self.assertEqual(self.player.frame_index, 0)
            self.assertFalse(self.player.paused)

    def test_large_delta_matches_small_steps(self):
        other = AnimationPlayer(self.animations)
        self.player.update(2 * 16.5 + 6.237)
        for _ in range(39237):
            other.update(.001)
        for key in ('animation_index', 'frame_index', 'completed_loops', 'paused'):
            self.assertEqual(getattr(self.player, key), getattr(other, key))
        self.assertAlmostEqual(self.player.elapsed, other.elapsed, places=7)

    def test_all_frames_are_large_and_fit_stage(self):
        scale = calculate_scale(self.data)
        for a in self.animations:
            for frame in a['frames']:
                x, y, w, h = frame_geometry(frame, scale)
                self.assertGreaterEqual(h, CANVAS_HEIGHT / 2)
                self.assertGreaterEqual(x-w/2, 24)
                self.assertLessEqual(x+w/2, 696)
                self.assertGreaterEqual(y-h/2, 96)
                self.assertLessEqual(y+h/2, 500)

    def test_reject_negative_elapsed_time(self):
        with self.assertRaises(ValueError):
            self.player.update(-1)

    def test_reject_invalid_clip(self):
        self.animations[0]['frames'][0]['x'] = self.data['width']
        with self.assertRaises(ValueError):
            validate_atlas(self.data)


if __name__ == '__main__':
    unittest.main()
