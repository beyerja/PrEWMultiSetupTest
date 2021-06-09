""" Numpy helper functions.
"""

import numpy as np

def is_symmetric(matrix, rtol=1e-05, atol=1e-08):
  """ Check if the matrix is symmetric within a given precision.
  """
  return np.allclose(matrix, matrix.T, rtol=rtol, atol=atol)