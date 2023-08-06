from abc import abstractmethod, ABCMeta


class abstract_trajectory_reader:
    __metaclass__ = ABCMeta

    """Provides a way to iterate through a molecular dynamics (MD) trajectory
    file.

    Each frame/time-step is returned as a trajectory_frame.
    """

    @classmethod
    @abstractmethod
    def available(cls):
        """ Returns True if this reader available on a particular system. """
        pass

    @abstractmethod
    def __iter__(self):
        """ Iterates through the trajectory file, frame by frame. """
        pass

    @abstractmethod
    def __next__(self):
        """ Gets next trajectory frame. """
        pass

    @abstractmethod
    def close(self):
        """ Closes down, release resources etc. """
        pass
