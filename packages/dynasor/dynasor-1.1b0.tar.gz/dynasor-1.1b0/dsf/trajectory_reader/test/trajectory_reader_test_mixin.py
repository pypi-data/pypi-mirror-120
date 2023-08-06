import numpy
import os

class TrajectoryReaderTestMixin(object):

    LAMMPSTRJ_FIRST_FRAME_FIRST_X = numpy.array([0.191468, 0.302071, 0.0528818])

    def filename_lammpstrj(self):
        data_path = self._data_dir_path()
        return os.path.join(data_path, "positions_and_velocities.lammpstrj")

    def filename_lammpstrj_no_velocities(self):
        data_path = self._data_dir_path()
        return os.path.join(data_path, "positions.lammpstrj")

    def filename_xtc_1frame_3atoms(self):
        data_path = self._data_dir_path()
        return os.path.join(data_path), "1frame3atoms.xtc"
    
    def assert_arrays_equal_within_float32eps(self, a, b):
        abs_diff = numpy.absolute(a - b)
        eps = self._float32abs()
        self.assertTrue((abs_diff < eps).all(),
                        "%s and %s not within eps from each other" % (a, b))

    def _data_dir_path(self):
        this_dir = os.path.dirname(__file__)
        return os.path.join(this_dir, "data")

    def _float32abs(self):
        return numpy.finfo(numpy.float32).eps
