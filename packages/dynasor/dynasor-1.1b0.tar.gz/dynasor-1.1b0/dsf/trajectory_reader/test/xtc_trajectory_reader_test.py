import unittest
from dsf.trajectory_reader.xtc_trajectory_reader import (
    xtc_trajectory_reader as trajectory_reader)
from dsf.trajectory_reader.test.trajectory_reader_test_mixin import TrajectoryReaderTestMixin


_not_available = not trajectory_reader.available()
_not_available_reason = "gromacs xtc plugin not available"

class XTCTrajectoryReaderTest(unittest.TestCase, TrajectoryReaderTestMixin):

    @unittest.skipIf(_not_available, _not_available_reason)
    def test_open_xtc(self):
        trajectory_reader(self.filename_xtc_1frame_3atoms())

    @unittest.skipIf(_not_available, _not_available_reason)
    def test_read_frames(self):
        reader = trajectory_reader(self.filename_xtc_1frame_3atoms())
        frames = list(reader)
        self.assertEqual(len(frames), 1)

    @unittest.skipIf(_not_available, _not_available_reason)
    def test_first_frame_contents(self):
        reader = trajectory_reader(self.filename_xtc_1frame_3atoms())
        frame = reader.next()
        self.assertEqual(frame['N'], 3)
        self.assertEqual(frame['v'], None)
        self.assert_arrays_equal_within_float32eps(frame['x'][:, 0],
                                                   self.XTC_FIRST_FRAME_FIRST_X)
