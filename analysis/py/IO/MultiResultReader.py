import logging as log
import numpy as np
from pathlib import Path
from tqdm import tqdm

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
  
  if not Path(file_path).is_file():
    log.debug("File not found.")
    return None
  
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
               lumi_setups, run_setups, muacc_setups, difparam_setups):
    self.setup_results = []
    
    log.info("Reading in setup results.")
    for lumi_setup in tqdm(lumi_setups):
      for run_setup in tqdm(run_setups, leave=False):
        for muacc_setup in tqdm(muacc_setups, leave=False):
          for difparam_setup in tqdm(difparam_setups, leave=False):
            setup_result = find_setup_result(result_dir, lumi_setup, run_setup, 
                                             muacc_setup, difparam_setup)
            # Only save result if it was found (meaning: not None)
            if setup_result:
              self.setup_results.append(setup_result)
                                
    self.setup_results = np.array(self.setup_results)
     
    n_found = len(self.setup_results)
    n_possible = len(lumi_setups) * len(run_setups) * len(muacc_setups)\
                 * len(difparam_setups)
    log.info("Found and read {} out of {} possible setup results.".format(
              n_found, n_possible))

  def get(self, lumi, run_name, muacc_name, difparam_name):
    """ Find a specific setup using the IDs for all the setup components.
    """
    found = np.array([setup for setup in self.setup_results 
                      if setup.equals(lumi,run_name,muacc_name,difparam_name)])
    if len(found) == 0:
      raise Exception("No setup found for {} {} {} {}".format(
                        lumi,run_name,muacc_name,difparam_name))
    if len(found) > 1:
      raise Exception("{} setups found for {} {} {} {}".format(
                        len(found),lumi,run_name,muacc_name,difparam_name))
    return found[0]
  
  def append(self, other_mrr):
    """ Add the results of another MultiResultReader to this one
    """
    self.setup_results = np.concatenate([self.setup_results, 
                                         other_mrr.setup_results])
    
def get_default_pol_mrr(result_dir):
  """ Get the default MultiResultReader that contains are current results for 
      runs with beam polarisation.
  """
  return MultiResultReader(result_dir, 
    SDS.default_lumi_setups, SDS.default_pol_run_setups,
    SDS.default_muacc_setups, SDS.default_pol_difparam_setups)
    
def get_default_unpol_mrr(result_dir):
  """ Get the default MultiResultReader that contains are current results for 
      runs without beam polarisation.
  """
  return MultiResultReader(result_dir, 
    SDS.default_lumi_setups, SDS.default_unpol_run_setups,
    SDS.default_muacc_setups, SDS.default_unpol_difparam_setups)
    
def get_default_mrr(result_dir):
  """ Get the default MultiResultReader that contains are current results.
  """
  full_mrr = get_default_pol_mrr(result_dir) 
  full_mrr.append(get_default_unpol_mrr(result_dir))
  return full_mrr