import logging as log

# Find and import the PrEW output reader
import IO.SysHelp as IOSH
IOSH.find_PrOut()
import PrOut

# Local modules
import IO.NamingConventions as IONC
import IO.SetupResult as IOSR
import Setups.DefaultSetups as SDS
         
def find_setup_result(result_dir, lumi_setup, run_setup, muacc_setup, 
                      difparam_setup):
  """ Find the setup result for the given setup combination in the given result
      directory.
  """
  file_name = IONC.infile_convention(lumi_setup, run_setup, muacc_setup, 
                                     difparam_setup)
  file_path = result_dir + "/" + file_name
  log.debug("Trying to read file " + file_path)
  reader = PrOut.Reader(file_path)
  reader.read()
  
  if (len(reader.run_results) != 1):
    raise Exception("Currently only able to read exactly 1 run setup per file,",
                    " found ", len(reader.run_results))

  result = reader.run_results[0]
  
  return IOSR.SetupResult(result, lumi_setup, run_setup, muacc_setup, 
                          difparam_setup)

class MultiResultReader:
  """ Class that can read in the outputs produced from a large number of runs 
      with different setups.
  """
  
  def __init__(self, result_dir, 
               lumi_setups = SDS.default_lumi_setups, 
               run_setups = SDS.default_run_setups, 
               muacc_setups = SDS.default_muacc_setups, 
               difparam_setups = SDS.default_difparam_setups):
    self.setup_results = []
    
    for lumi_setup in lumi_setups:
      for run_setup in run_setups:
        for muacc_setup in muacc_setups:
          for difparam_setup in difparam_setups:
            self.setup_results.append(
              find_setup_result(result_dir, lumi_setup, run_setup, muacc_setup, 
                                difparam_setup))            
  
    log.info("Found and read {} setup results.".format(len(self.setup_results)))


