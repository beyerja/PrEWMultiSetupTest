import logging as log
import numpy as np

# Local modules
import Analysis.CovMatrixCalc as ACMC
import Analysis.NumpyHelp as ANH

class ResultSummary:
  """ Class that calculate a summary for a given run result.
  """
  
  def __init__(self, run_result):
    result_vals = np.array([fr.pars_fin for fr in run_result.fit_results])    
    self.par_names = run_result.par_names
    
    # Parameter result range related things
    self.par_vals = np.array([fr.pars_fin for fr in run_result.fit_results])
    self.par_avg = np.average(self.par_vals, axis=0)
    self.par_min = np.amin(self.par_vals, axis=0)
    self.par_max = np.amax(self.par_vals, axis=0)
    
    # Covariance matrix related things
    self.cov_mat = ACMC.calc_cov_mat(result_vals)
    self.cor_mat = ACMC.calc_cor_mat(self.cov_mat)
    self.unc_vec = ACMC.calc_std_dev(self.cov_mat)
    self.fit_unc_avg = np.average(np.array([fr.uncs_fin for fr in run_result.fit_results]), axis=0)
    self.consistency_check()
    
    # Fit behaviour related things
    self.ndf = run_result.fit_results[0].n_bins - run_result.fit_results[0].n_free_pars
    self.nll = np.array([fr.chisq_fin for fr in run_result.fit_results])
    self.cov_status = np.array([fr.cov_status for fr in run_result.fit_results])
    self.min_status = np.array([fr.min_status for fr in run_result.fit_results])
    self.fct_calls = np.array([fr.n_fct_calls for fr in run_result.fit_results])
    self.n_iters = np.array([fr.n_iters for fr in run_result.fit_results])
    
  def consistency_check(self):
    """ Perform some simple consistency check to see if calculated covariance 
        makes sense and is somewhat constistence with what the fit says.
    """
    # Is covariance matrix symmetric
    if not ANH.is_symmetric(self.cov_mat):
      log.warning("Covariance matrix not symmetric ", self.cov_mat)
    
    # Are calculated uncertainties equal to those found by fit?
    rel_tolerance = 0.15
    if not np.allclose(self.fit_unc_avg,self.unc_vec,rtol=rel_tolerance):
      log.debug("Calculated uncertainty deviates more than {}% from the one that the fit calculated.".format(rel_tolerance*100))
      log.debug("Own calc: {}".format(self.unc_vec))
      log.debug("Fit calc: {}".format(self.fit_unc_avg))
      
      
  # TODO TODO TODO
  # Make this directly writable so it can be written to a summary text file for each access
  # TODO: Leave out par vals
  # TODO: Summarize nll, cov_status, min_status, fct_calls, n_iters
  # TODO TODO TODO