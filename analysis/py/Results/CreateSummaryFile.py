import logging as log
import os
import sys

# Local modules
sys.path.append("..") # Use the modules in the top level directory
import Analysis.ResultSummary as ARS
import IO.MultiResultReader as IOMRR
import IO.NamingConventions as IONC
import IO.SysHelp as IOSH

""" Create a summary file that contains the a readable summary for each setup.
"""

log.basicConfig(level=log.INFO) # Set logging level
os.environ["USE_N_CORES"] = "7"

output_base = "../../../output"
fit_output_base = "{}/run_outputs".format(output_base)
msr = IOMRR.get_default_mrr(fit_output_base)

# Output directory
summary_dir = "{}/summary".format(output_base)

# Open a file to write out the uncertainties and cor matrix summary
IOSH.create_dir(summary_dir)
file = open(summary_dir + "/result_summary.txt", "w")

# Write each result
for res in msr.setup_results:
  setup_out_name = IONC.setup_convention(res.lumi_setup, res.run_setup, 
                                         res.muacc_setup, res.difparam_setup, 
                                         res.WW_setup)
  log.info("Checking: {}".format(setup_out_name))
  
  # Calculate a summary of the result (e.g. cor matrix, unc., ...)
  res_summary = ARS.ResultSummary(res.run_result)
  
  # Write summary to the output file
  file.write(setup_out_name + "\n")
  file.write(str(res_summary) + "\n\n")
  
file.close()