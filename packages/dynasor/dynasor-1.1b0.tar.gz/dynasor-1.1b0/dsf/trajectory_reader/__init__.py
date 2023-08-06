from .lammpstrj_trajectory_reader import lammpstrj_trajectory_reader
from .molfile_trajectory_reader import molfile_trajectory_reader
from .xtc_trajectory_reader import xtc_trajectory_reader

available_readers = []

for reader in [lammpstrj_trajectory_reader,
               molfile_trajectory_reader,
               xtc_trajectory_reader]:
    if reader.available():
        available_readers.append(reader)
