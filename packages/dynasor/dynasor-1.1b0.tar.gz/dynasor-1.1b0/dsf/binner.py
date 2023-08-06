__all__ = ['fixed_bin_averager']

import numpy as np
import logging

logger = logging.getLogger('dynasor')


class fixed_bin_averager:

    """
    Class for averaging data sets of points (x,y) with a priori decided
    positions (x), over a pre-defined number of equally sized, linearely
    distriuted bins.

    This is used to get an average of y for a set of lineary spaced x values
    when a possibly large set of {y(x)} is given.

    The result will be an array containing, for each bin, the average y-value
    over the data points having its x-value within the respective bin x-range.
    """

    def __init__(self, x_max, x_bins, x_distances, x_min=0.0):
        assert x_max > x_min
        assert x_bins > 1

        self.delta_x = (x_max-x_min) / (x_bins-1)
        x_range = (x_min-self.delta_x/2, x_max+self.delta_x/2)
        bin_count, edges = np.histogram(x_distances,
                                        bins=x_bins,
                                        range=x_range)
        self.x_linspace = 0.5 * (edges[1:]+edges[:-1])

        m = np.nonzero(bin_count)
        self.bin_count = bin_count[m]
        self.x = self.x_linspace[m]
        self.input_length = len(x_distances)
        self.bins = len(self.x)
        if self.bins != x_bins:
            logger.info('Ignoring {} bins without coverage'
                        .format(x_bins-self.bins))

    def bin(self, y, axis=0):
        y = np.require(y)
        assert y.shape[axis] == self.input_length

        res_shape = list(y.shape)
        res_shape[axis] = self.bins
        result = np.zeros(res_shape)

        ci = 0
        ind_x = [slice(None)]*len(y.shape)
        ind_y = [slice(None)]*len(y.shape)
        for i, n in enumerate(self.bin_count):
            ind_x[axis] = i
            ind_y[axis] = slice(ci, ci+n)
            result[tuple(ind_x)] = np.mean(y[tuple(ind_y)], axis=axis)
            ci += n

        return result
