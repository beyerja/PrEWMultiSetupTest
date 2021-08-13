import logging as log
import multiprocessing as mp
import os
import sys
from tqdm import tqdm

# Local modules
sys.path.append("..") # Use the modules in the top level directory
import Analysis.ResultSummary as ARS
import MultiProc.ConfigHelp as MPCH
import IO.MultiResultReader as IOMRR
import IO.NamingConventions as IONC
import Plotting.DefaultFormat as PDF
import Plotting.SetupPlotting as PSP

""" Create the individual summary plots for each result, e.g. the covariance 
    matrix, the fit behavious, the individual parameter plots, ...
"""

log.basicConfig(level=log.INFO) # Set logging level
os.environ["USE_N_CORES"] = "10"

output_base = "../../../output"
fit_output_base = "{}/run_outputs".format(output_base)
msr = IOMRR.get_default_mrr(fit_output_base)

# Output directories
plot_base = "{}/plots".format(output_base)

# Set the default matplotlib formatting
PDF.set_default_mpl_format()

# Create summary plots for each result (using parallel programming)
os.environ["USE_N_CORES"] = "4" # Reduce the number of cores (goes crazy else)
pool = mp.Pool(MPCH.get_n_cores())
result_objects = []

log.info("Starting processes to create plots for each setup.")
for res in tqdm(msr.setup_results):
  setup_out_name = IONC.setup_convention(res.lumi_setup, res.run_setup, 
                                         res.muacc_setup, res.difparam_setup,
                                         res.WW_setup)
  log.debug("Checking: {}".format(setup_out_name))
  
  # Calculate a summary of the result (e.g. cor matrix, unc., ...)
  res_summary = ARS.ResultSummary(res.run_result)
  
  # Create all the summary plots for this setup (in parallel process)
  plot_dir = "{}/SingleSetup/{}".format(plot_base,setup_out_name)
  result_objects.append(
    pool.apply_async(PSP.plot_res_summary, args=(res_summary,plot_dir)))
  
# "get" the result to get a tqdm counter of them finishing
log.info("Running processes.")
for r in tqdm(result_objects):
  _ = r.get()
  
# Let all processes finish
pool.close()
pool.join()
log.info("Done!")