import logging as log
import numpy as np

# Local modules
import Analysis.CovMatrixCalc as ACMC
import Analysis.NumpyHelp as ANH

class ResultSummary:
  """ Class that calculate a summary for a given run result.
  """
  
  def __init__(self, run_result):
    self.par_names = np.array(run_result.par_names)
    
    # Parameter result range related things
    self.par_vals = np.array([fr.pars_fin for fr in run_result.fit_results])
    self.par_avg = np.average(self.par_vals, axis=0)
    self.par_min = np.amin(self.par_vals, axis=0)
    self.par_max = np.amax(self.par_vals, axis=0)
    
    # Covariance matrix related things
    result_vals = np.array([fr.pars_fin for fr in run_result.fit_results])    
    self.cov_mat_calc = ACMC.calc_cov_mat(result_vals) # TODO Check where this was used and replace everywhere!
    self.cor_mat_calc = ACMC.calc_cor_mat(self.cov_mat_calc)
    self.unc_vec_calc = ACMC.calc_std_dev(self.cov_mat_calc)
    self.cov_mat_avg = np.average(np.array([fr.cov_matrix for fr in run_result.fit_results]), axis=0)
    self.cor_mat_avg = np.average(np.array([fr.cor_matrix for fr in run_result.fit_results]), axis=0)
    self.unc_vec_avg = np.average(np.array([fr.uncs_fin for fr in run_result.fit_results]), axis=0)
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
    if not ANH.is_symmetric(self.cov_mat_calc):
      log.warning("Covariance matrix not symmetric ", self.cov_mat_calc)
    
    # Are calculated uncertainties equal to those found by fit?
    rel_tolerance = 0.15
    if not np.allclose(self.unc_vec_avg,self.unc_vec_calc,rtol=rel_tolerance):
      log.debug("Calculated uncertainty deviates more than {}% from the one that the fit calculated.".format(rel_tolerance*100))
      log.debug("Own calc: {}".format(self.unc_vec_calc))
      log.debug("Fit calc: {}".format(self.unc_vec_avg))
      
  def par_index(self, par_name):
    """ Return the index of the given parameter.
    """  
    indices = np.where(self.par_names == par_name)[0]
    if len(indices) == 0:
      raise Exception("No parameter {} found.".format(par_name))
    elif len(indices) > 1:
      raise Exception("{} parmeters {} found.".format(par_name))
    return indices[0]
    
  def unc(self, par_name):
    """ Return the uncertainty for the given parameter.
    """
    return self.unc_vec_calc[self.par_index(par_name)]
      
  def fit_unc(self, par_name):
    """ Return the uncertainty for the given parameter.
    """
    return self.unc_vec_avg[self.par_index(par_name)]
      
  def __str__(self):
    """ Make this class printable.
    """
    np.set_printoptions(linewidth=999999) # Avoid extra line breaks
    out =  "Par. names  : {}\n".format(self.par_names)
    out += "Par. results: {}\n".format(self.par_avg)
    out += "Calc.    unc: {}\n".format(self.unc_vec_calc)
    out += "Avg. fit unc: {}\n".format(self.unc_vec_avg)
    out += "Avg. cor.mat.:\n{}\n".format(self.cor_mat_avg)
    
    out += "Avg. NLL/ndf: {}\n".format(np.average(self.nll)/self.ndf)
    out += "Cov. status: "
    for status in np.arange(-1,4):
      out +="{}: {}, ".format(status,(self.cov_status == status).sum())
    out += "\n"
    out += "Min. status: "
    for status in np.arange(-1,7):
      out +="{}: {}, ".format(status,(self.min_status == status).sum())
    out += "\n"
    out += "Avg. fct. calls: {}".format(np.average(self.fct_calls))
    np.set_printoptions(linewidth=75) # Reset to default
    return out