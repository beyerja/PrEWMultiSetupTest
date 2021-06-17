import logging as log
import sys

# Local modules
sys.path.append("..") # Use the modules in the top level directory
import Analysis.ResultSummary as ARS
import IO.MultiResultReader as IOMRR
import IO.NamingConventions as IONC
import Plotting.DefaultFormat as PDF
import Plotting.SetupPlotting as PSP

""" Create the individual summary plots for each result, e.g. the covariance 
    matrix, the fit behavious, the individual parameter plots, ...
"""

log.basicConfig(level=log.INFO) # Set logging level
output_base = "../../../output"
fit_output_base = "{}/run_outputs".format(output_base)
msr = IOMRR.MultiResultReader(fit_output_base)

# Output directories
plot_base = "{}/plots".format(output_base)

# Set the default matplotlib formatting
PDF.set_default_mpl_format()

# Create summary plots for each result
for res in msr.setup_results:
  setup_out_name = IONC.setup_convention(res.lumi_setup, res.run_setup, res.muacc_setup, res.difparam_setup)
  log.info("Checking: {}".format(setup_out_name))
  
  # Calculate a summary of the result (e.g. cor matrix, unc., ...)
  res_summary = ARS.ResultSummary(res.run_result)
  
  # Create all the summary plots for this setup
  plot_dir = "{}/SingleSetup/{}".format(plot_base,setup_out_name)
  PSP.plot_res_summary(res_summary,plot_dir)