import unittest
from dsf.trajectory_reader.lammpstrj_trajectory_reader \
    import lammpstrj_trajectory_reader as trajectory_reader
from dsf.trajectory_reader.test.trajectory_reader_test_mixin \
    import TrajectoryReaderTestMixin


_not_available = not trajectory_reader.available()
_not_available_reason = 'lammpstrj plugin not available'


class LAMMPSTRJTrajectoryReaderTest(unittest.TestCase,
                                    TrajectoryReaderTestMixin):

    @unittest.skipIf(_not_available, _not_available_reason)
    def test_open_lammpstrj_no_velocities(self):
        trajectory_reader(self.filename_lammpstrj_no_velocities())

    @unittest.skipIf(_not_available, _not_available_reason)
    def test_open_lammpstrj(self):
        trajectory_reader(self.filename_lammpstrj())

    @unittest.skipIf(_not_available, _not_available_reason)
    def test_read_frames(self):
        reader = trajectory_reader(self.filename_lammpstrj())
        frames = list(reader)
        self.assertEqual(len(frames), 4)

    @unittest.skipIf(_not_available, _not_available_reason)
    def test_first_frame_contents(self):
        reader = trajectory_reader(self.filename_lammpstrj())
        frame = next(reader)
        self.assertEqual(frame['N'], 24)
        self.assert_arrays_equal_within_float32eps(
            frame['x'][:, 0], self.LAMMPSTRJ_FIRST_FRAME_FIRST_X)

    @unittest.skipIf(_not_available, _not_available_reason)
    def test_first_frame_contents_no_velocities(self):
        reader = trajectory_reader(self.filename_lammpstrj_no_velocities())
        frame = next(reader)
        self.assertEqual(frame['N'], 24)
        self.assertEqual(frame['v'], None)
        self.assert_arrays_equal_within_float32eps(
            frame['x'][:, 0], self.LAMMPSTRJ_FIRST_FRAME_FIRST_X)
