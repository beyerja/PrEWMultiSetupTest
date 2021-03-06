# Find and import the PrEW output reader
import IO.SysHelp as IOSH
IOSH.find_PrOut()
import PrOut

import Analysis.ResultSummary as ARS

class SetupResult:
  """ Class that stores the results and metadata of a single fit setup.
  """
  def __init__(self, run_result, lumi_setup, run_setup, muacc_setup, 
               difparam_setup, WW_setup):
    self.run_result = run_result
    self.lumi_setup = lumi_setup
    self.run_setup = run_setup
    self.muacc_setup = muacc_setup
    self.difparam_setup = difparam_setup
    self.WW_setup = WW_setup
    
  def equals(self, lumi, run_name, muacc_name, difparam_name, WW_name):
    """ Is this result described by the given ID's for all the setup options.
    """
    return (self.lumi_setup == lumi) and\
           (self.run_setup.name == run_name) and\
           (self.muacc_setup.name == muacc_name) and\
           (self.difparam_setup.name == difparam_name) and\
           (self.WW_setup.name == WW_name)
           
  def result_summary(self):
    """ Get the result summary for this setup.
    """
    return ARS.ResultSummary(self.run_result)