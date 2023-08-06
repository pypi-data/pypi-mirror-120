class trajectory_frame(object):
    """Trivial data struct holding MD-data for one time frame

     'index' : trajectory index,
     'box'   : simulation box as 3 row vectors (nm),
     'N'     : number of atoms,
     'x'     : particle positions as 3xN array (nm),
     'v'     : (*) particle velocities as 3xN array (nm/ps),
     'time'  : (*) simulation time (ps),

     (*) may not be available, depends on reader and trajectory file format.
    """
    def __init__(self, **kwargs):
        for attribute, value in kwargs.iteritems():
            setattr(self, attribute, value)
