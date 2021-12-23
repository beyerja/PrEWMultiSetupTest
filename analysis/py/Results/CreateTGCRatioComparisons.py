import logging as log
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
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

def draw_ratios(ax, rs_pol, rs_unpol, x_shift, **kwargs):
  """ Draw the unpolarised/polarised ratio for given polarised and unpolarised 
      results.
  """
  x = np.arange(3)+0.5+x_shift
  
  # Find the uncertainties
  g_unc_pol = rs_pol.fit_unc("Delta-g1Z")
  k_unc_pol = rs_pol.fit_unc("Delta-kappa_gamma")
  l_unc_pol = rs_pol.fit_unc("Delta-lambda_gamma")
  g_unc_unpol = rs_unpol.fit_unc("Delta-g1Z")
  k_unc_unpol = rs_unpol.fit_unc("Delta-kappa_gamma")
  l_unc_unpol = rs_unpol.fit_unc("Delta-lambda_gamma")
        
  y = np.array([
    g_unc_unpol / g_unc_pol,
    k_unc_unpol / k_unc_pol,
    l_unc_unpol / l_unc_pol
  ])
    
  # Plot the uncertainties
  ax.plot(x, y, **kwargs)

#-------------------------------------------------------------------------------

def TGC_ratio_plot(mrr, output_dir):
  """ Make plot of the uncertainty ratios unpolarised/polarised for various 
      polarised scenarios and for ALR free or fixed.
  """
  fig = plt.figure(figsize=(8,6), tight_layout=True)
  
  x = np.arange(3)+0.5
  x_ticks = [ "$g_{1}^{Z}$", "$\kappa_{\gamma}$", "$\lambda_{\gamma}$" ]
  plt.xticks(x, x_ticks, size='large')
  
  # plt.xlabel('Triple Gauge Couplings', size='large')
  ax = plt.gca()
  ax.set_xlim(-0.3, 3)
  ax.set_ylabel(r"Uncertainty ratio: $\frac{unpolarised}{polarised}$", size='large')
  
  rs_0pol_ALRfixd = mrr.get(2000, "0pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary()
  rs_1pol_ALRfixd = mrr.get(2000, "1pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary()
  rs_2pol_ALRfixd = mrr.get(2000, "2pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary()
  rs_2polExt_ALRfixd = mrr.get(2000, "2polExt_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary()
  rs_0pol_ALRfree = mrr.get(2000, "0pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFree").result_summary()
  rs_1pol_ALRfree = mrr.get(2000, "1pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFree").result_summary()
  rs_2pol_ALRfree = mrr.get(2000, "2pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFree").result_summary()
  rs_2polExt_ALRfree = mrr.get(2000, "2polExt_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFree").result_summary()
  
  # Get the colors of the color cycle (to get manual control over them)
  colors =  plt.rcParams['axes.prop_cycle'].by_key()['color']
  
  draw_ratios(ax, rs_2polExt_ALRfixd, rs_0pol_ALRfixd, -0.2, color=colors[0], ls="", ms=15, marker="v")
  draw_ratios(ax, rs_2pol_ALRfixd, rs_0pol_ALRfixd, 0,       color=colors[1], ls="", ms=15, marker="v")
  draw_ratios(ax, rs_1pol_ALRfixd, rs_0pol_ALRfixd, 0.2,     color=colors[2], ls="", ms=15, marker="v")
  draw_ratios(ax, rs_2polExt_ALRfree, rs_0pol_ALRfree, -0.2, color=colors[0], ls="", ms=15, marker="v", fillstyle="none")
  draw_ratios(ax, rs_2pol_ALRfree, rs_0pol_ALRfree, 0,       color=colors[1], ls="", ms=15, marker="v", fillstyle="none")
  draw_ratios(ax, rs_1pol_ALRfree, rs_0pol_ALRfree, 0.2,     color=colors[2], ls="", ms=15, marker="v", fillstyle="none")

  ax.set_ylim(1.0,ax.get_ylim()[1])
  ax.set_yticks([1.0,1.5,2.0])
  
  ax.text(-0.2, 1.92, "(80/0,\n 30/0)", color=colors[0])
  ax.text(0.4, 1.95, "(80,30)", color=colors[1])
  ax.text(0.6, 1.6, "(80,0)", color=colors[2])
  
  ax.text(-0.1, 1.75, "$A_{LR}$\nfree", color='white', path_effects=[pe.withStroke(linewidth=1, foreground="black")])
  ax.text(-0.1, 1.3, "$A_{LR}$\nfixed", color="black")

  for out_format in ["pdf","png"]:
    format_dir = "{}/{}".format(output_dir,out_format)
    IOSH.create_dir(format_dir)
    fig.savefig("{}/TGC_ratios.{}".format(format_dir,out_format), transparent=True)
  plt.close(fig)

#-------------------------------------------------------------------------------

def main():
  log.basicConfig(level=log.INFO)
  PDF.set_default_mpl_format()
  os.environ["USE_N_CORES"] = "7"
  
  output_base = "../../../output"
  fit_output_base = "{}/run_outputs".format(output_base)
  
  lumi_setups = [ 2000 ]
  pol_run_setups = [
    IORS.RunSetup("2polExt_LPcnstr"),
    IORS.RunSetup("2pol_LPcnstr"),
    IORS.RunSetup("1pol_LPcnstr"),
  ]
  unpol_run_setups = [
    IORS.RunSetup("0pol_LPcnstr")
  ]
  muacc_setups = [
    IOMAS.MuAccSetup("MuAccFree")
  ]
  WW_setups = [
    IOWWS.WWSetup("WWcTGCs_xs0Free_AFree"),
    IOWWS.WWSetup("WWcTGCs_xs0Free_AFixd")
  ]
  
  mrr = IOMRR.MultiResultReader(fit_output_base, lumi_setups, 
                                pol_run_setups, muacc_setups, 
                                WW_setups=WW_setups)
  mrr.append(IOMRR.MultiResultReader(fit_output_base, lumi_setups, 
                                     unpol_run_setups, muacc_setups, 
                                     WW_setups=WW_setups))

  # Output directories
  output_dir = "{}/plots/TGCRatioComparison".format(output_base)

  TGC_ratio_plot(mrr, output_dir)
  
if __name__ == "__main__":
  main()
