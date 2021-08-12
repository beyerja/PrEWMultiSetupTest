""" Functions and classes to help with configuring the multiprocessing setup.
"""

import multiprocessing as mp
import numpy as np
import os

def get_n_cores():
  """ Return the number of cores that is supposed to be used.
      Can be defined anywhere else by setting the USE_N_CORES variable with e.g.
        os.environ["USE_N_CORES"] = "7"
      default: 1/3 of available cores (rounded up)
  """
  n_cores = np.ceil(mp.cpu_count() / 3)
  if "USE_N_CORES" in os.environ:
    n_cores = os.environ["USE_N_CORES"]
  return int(n_cores)

