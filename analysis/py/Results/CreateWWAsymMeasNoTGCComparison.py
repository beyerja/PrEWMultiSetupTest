from decimal import Decimal
import logging as log
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# Local modules
sys.path.append("..") # Use the modules in the top level directory
import IO.MultiResultReader as IOMRR
import IO.SysHelp as IOSH
import Plotting.DefaultFormat as PDF
import Setups.MuAccSetup as IOMAS
import Setups.RunSetup as IORS
import Setups.WWSetup as IOWWS

#-------------------------------------------------------------------------------

def get_comb_asymm_unc(rs):
  """ TGC impact of asymmetry is symmetric for mu+ and mu-, so that the relevant
      uncertainty is the combined uncertainty.
  """
  unc_M = rs.fit_unc("DeltaA_WW_muminus")
  unc_P = rs.fit_unc("DeltaA_WW_muplus")
  return 1/2 * np.sqrt( unc_M**2 + unc_P**2 )

def WW_par_plot(mrr, output_dir, scale):
  fig = plt.figure(tight_layout=True, figsize=(8.8,6.5))
  ax = plt.gca()
  

  # colors =  plt.rcParams['axes.prop_cycle'].by_key()['color']
  
  x = np.arange(5)+0.5
  x_ticks = ( "$2$ab$^{-1}$\n$(80/0,$\n $30/0)$",
              "$2$ab$^{-1}$\n$(80,30)$",
              "$2$ab$^{-1}$\n$(80,0)$",
              "$2$ab$^{-1}$\n$(0,0)$",
              "$10$ab$^{-1}$\n$(0,0)$" )
  plt.xticks(x, x_ticks, size='large')
  ax.set_xlim(0,x[-1]+0.5)
  ax.set_ylim(0,3.5)
  # ax.set_xlabel('$WW$ cross section parameters', size='large')
  ax.set_ylabel('$\Delta A_{{comb.}}$ [{:.0E}]'.format(Decimal(scale)), size='large')
  
  y_polfree = np.array([
    get_comb_asymm_unc(rs) for rs in (
      mrr.get(2000, "2polExt_LPcnstr", "MuAccFree", WW_name="WW_xs0Free_AFree").result_summary(),
      mrr.get(2000, "2pol_LPcnstr", "MuAccFree", WW_name="WW_xs0Free_AFree").result_summary(),
      mrr.get(2000, "1pol_LPcnstr", "MuAccFree", WW_name="WW_xs0Free_AFree").result_summary(),
      mrr.get(2000, "0pol_LPcnstr", "MuAccFree", WW_name="WW_xs0Free_AFree").result_summary(),
      mrr.get(10000, "0pol_LPcnstr", "MuAccFree", WW_name="WW_xs0Free_AFree").result_summary()
      ) ]) / scale

  for s in range(len(x)):
    ax.bar((x[s]), (y_polfree[s]), width=0.5, align='center', zorder=2)

  ax.legend(title="Fit w/o TGCs", title_fontsize=28)
  
  # Reduce the number of axis ticks
  ax.locator_params(axis='y', nbins=4)

  for out_format in ["pdf","png","eps"]:
    format_dir = "{}/{}".format(output_dir,out_format)
    IOSH.create_dir(format_dir)
    fig.savefig("{}/WWAsymmMeasurementNoTGC.{}".format(format_dir,out_format), transparent=True)
  plt.close(fig)


#-------------------------------------------------------------------------------

def main():
  log.basicConfig(level=log.INFO)
  PDF.set_default_mpl_format()
  os.environ["USE_N_CORES"] = "7"
  
  output_base = "../../../output"
  fit_output_base = "{}/run_outputs".format(output_base)
  
  pol_lumi_setups = [ 2000 ]
  unpol_lumi_setups = [ 2000, 10000 ]
  pol_run_setups = [
    IORS.RunSetup("2polExt_LPcnstr"),
    IORS.RunSetup("2polExt_Lconstr_Pfixed"),
    IORS.RunSetup("2pol_LPcnstr"),
    IORS.RunSetup("2pol_Lconstr_Pfixed"),
    IORS.RunSetup("1pol_LPcnstr"),
    IORS.RunSetup("1pol_Lconstr_Pfixed"),
  ]
  unpol_run_setups = [
    IORS.RunSetup("0pol_LPcnstr"),
    IORS.RunSetup("0pol_Lconstr_P0fixed"),
  ]
  muacc_setups = [
    IOMAS.MuAccSetup("MuAccFree"),
  ]
  WW_setups = [
    IOWWS.WWSetup("WW_xs0Free_AFree")
  ]
  
  mrr = IOMRR.MultiResultReader(fit_output_base, pol_lumi_setups, 
                                pol_run_setups, muacc_setups, 
                                WW_setups=WW_setups)
  mrr.append(IOMRR.MultiResultReader(fit_output_base, unpol_lumi_setups, 
                                     unpol_run_setups, muacc_setups, 
                                     WW_setups=WW_setups))

  # Output directories
  output_dir = "{}/plots/WWAsymmNoTGC".format(output_base)

  scale = 1.e-4
  WW_par_plot(mrr, output_dir, scale)
  
if __name__ == "__main__":
  main()
