""" Naming conventions for files names, directories, etc.
"""

def setup_convention(lumi_setup, run_setup, muacc_setup, difparam_setup):
  """ General convention marking a specific setup.
  """
  return "{}_L{}_{}_{}".format(run_setup.name, int(lumi_setup), 
                               muacc_setup.name, difparam_setup.name)

def infile_convention(lumi_setup, run_setup, muacc_setup, difparam_setup):
  """ The convention for a fit result file name, depending on the setup.
  """
  return "fit_results_{}.out".format(
           setup_convention(lumi_setup, run_setup, muacc_setup, difparam_setup))
         