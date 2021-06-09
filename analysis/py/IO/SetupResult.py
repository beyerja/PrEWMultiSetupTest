# Find and import the PrEW output reader
import IO.SysHelp as IOSH
IOSH.find_PrOut()
import PrOut

class SetupResult:
  """ Class that stores the results and metadata of a single fit setup.
  """
  def __init__(self, run_result, lumi_setup, run_setup, muacc_setup, difparam_setup):
    self.run_result = run_result
    self.lumi_setup = lumi_setup
    self.run_setup = run_setup
    self.muacc_setup = muacc_setup
    self.difparam_setup = difparam_setup
  