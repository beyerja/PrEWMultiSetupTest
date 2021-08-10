""" Naming conventions for files names, directories, etc.
"""

import Setups.DifParamSetup as IODPS
import Setups.WWSetup as IOWWS

def setup_convention(lumi_setup, run_setup, muacc_setup, 
                     difparam_setup=IODPS.DifParamSetup(), 
                     WW_setup=IOWWS.WWSetup()):
  """ General convention marking a specific setup.
  """
  name = "{}_L{}_{}".format(run_setup.name, int(lumi_setup), muacc_setup.name)
  if difparam_setup.name:
    name += "_" + difparam_setup.name
  if WW_setup.name:
    name += "_" + WW_setup.name
  return name

def infile_convention(lumi_setup, run_setup, muacc_setup, 
                      difparam_setup=IODPS.DifParamSetup(), 
                      WW_setup=IOWWS.WWSetup()):
  """ The convention for a fit result file name, depending on the setup.
  """
  return "fit_results_{}.out".format(
           setup_convention(lumi_setup, run_setup, muacc_setup, difparam_setup, 
                            WW_setup))
         