""" Functions for the calculation of the covariance matrix of a fit and related 
    helper functions.
"""

import numpy as np

def calc_cov_mat(result_vals):
  """ Calculate the covariance matrix for the given fits.
      For each of the N fits, the final result values x of all M parameters are 
      given.
      The covariance matrix is then calculated by the unbiased estimator:
        Q_ij = 1/(N-1) Sum_k=1^M (x_i^k - avg(x_i))*(x_j^k - avg(x_j))
  """
  if (result_vals.ndim != 2):
    raise Exception("Result array needs to be 2D, is ",result_vals.dim)
    
  n_fits = len(result_vals)
  if (n_fits < 2):
    raise Exception("Need at least two result to estimate covariance matrix.")
  
  avgs = np.average(result_vals,axis=0)
  val_m_avg = result_vals - avgs
  return np.matmul(np.transpose(val_m_avg),val_m_avg) / (n_fits - 1.)
  
def calc_std_dev(cov_mat):
  """ Calculate the standard deviations of the parameters for the given 
      covariance matrix.
  """
  return np.sqrt(np.diagonal(cov_mat))
  
def calc_cor_mat(cov_mat):
  """ Calculate the correlation matrix for the given covariance matrix.
  """
  std_dev = calc_std_dev(cov_mat)
  norm = np.outer(std_dev,std_dev)
  
  # Avoid devide-by-zero errors and numerical fluctuations 
  # (e.g. for fixed parameters)
  norm += 1.0 * (np.abs(norm) < 1.e-12)
  
  return cov_mat / norm * (np.abs(norm) > 1.e-12)