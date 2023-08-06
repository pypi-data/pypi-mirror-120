__all__ = ['create_mfile', 'create_pfile']

import sys
import numpy as np
import logging

logger = logging.getLogger('dynasor')


def create_mfile(filename, output, comment=None):
    """ Creates matlab style m-file. """
    with open(filename, 'w') as fh:
        popts = np.get_printoptions()
        np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

        if comment is not None:
            fh.write('%%%\n')
            fh.write(''.join(['% '+x+'\n' for x in comment.split('\n')]))
            fh.write('%%%\n')

        for v, n, desc in output:
            fh.write("\n%% %s\n%s = ...\n%s;\n" % (desc, n, str(v)))

        np.set_printoptions(**popts)
        logger.info('Wrote Matlab-style output to {}'.format(fh.name))


def create_pfile(filename, output, comment=None):
    """ Creates python pickle file. """
    import pickle
    with open(filename, 'wb') as fh:
        pickle.dump(output, fh)
        logger.info('Wrote pickled output to {}'.format(fh.name))
