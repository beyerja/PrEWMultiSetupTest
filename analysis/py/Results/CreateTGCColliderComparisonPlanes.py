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
import Plotting.Statistics as PS
import Setups.MuAccSetup as IOMAS
import Setups.RunSetup as IORS
import Setups.WWSetup as IOWWS

#-------------------------------------------------------------------------------
  
def draw_ellipse(ax, rs, c1_name, c2_name, scale=1., **kwargs):
  """ Draw the uncertainty ellipse from the result summary for the two given 
      couplings.
  """
  i_c1 = rs.par_index(c1_name)
  i_c2 = rs.par_index(c2_name)
  full_cov = rs.cov_mat_avg
  c1c2_cov = np.array([[full_cov[i_c1,i_c1],full_cov[i_c2,i_c1]],
                       [full_cov[i_c1,i_c2],full_cov[i_c2,i_c2]]]) / scale**2
                       
  PS.confidence_ellipse(c1c2_cov, 0, 0, ax, n_std=1.0, **kwargs)

def draw_setups(mrr, ax, c1_name, c2_name, scale=1, set_labels=False):
  """ Plot the uncertainty ellipses between the two given couplings for all 
      collider scenarios.
  """
  # Recover all result summaries 
  rs_2polExt = mrr.get(2000, "2polExt_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary()
  rs_2pol = mrr.get(2000, "2pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary()
  rs_1pol = mrr.get(2000, "1pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary()
  rs_0pol_2 = mrr.get(2000, "0pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary()
  rs_0pol_10 = mrr.get(10000, "0pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary()

  # Get the colors of the color cycle (to get manual control over them)
  colors =  plt.rcParams['axes.prop_cycle'].by_key()['color']
  
  labels = [None for i in range(5)]
  if set_labels:
    labels = [
      "(80,0), 2ab$^{-1}$",
      "(80,30), 2ab$^{-1}$",
      "(80/0,30/0), 2ab$^{-1}$",
      "(0,0), 2ab$^{-1}$",
      "(0,0), 10ab$^{-1}$"
    ]
    
  # Draw the polarised setups as ellipses
  draw_ellipse(ax, rs_1pol, c1_name, c2_name, scale=scale, ls="-", lw=5.0, edgecolor=colors[2], facecolor='none', label=labels[0])
  draw_ellipse(ax, rs_2pol, c1_name, c2_name, scale=scale, ls="-", lw=5.0, edgecolor=colors[1], facecolor='none', label=labels[1])
  draw_ellipse(ax, rs_2polExt, c1_name, c2_name, scale=scale, ls="-", lw=4.0, edgecolor=colors[0], facecolor='none', label=labels[2])
  draw_ellipse(ax, rs_0pol_2, c1_name, c2_name, scale=scale, ls="-", lw=5.0, edgecolor=colors[3], facecolor='none', label=labels[3])
  draw_ellipse(ax, rs_0pol_10, c1_name, c2_name, scale=scale, ls="-", lw=5.0, edgecolor=colors[4], facecolor='none', label=labels[4])

#-------------------------------------------------------------------------------

def reorder_legend_handles(ax):
  """ Reorder the legend handles to make the legend look more orderly.
  """
  handles, _ = ax.get_legend_handles_labels()
  reordering = [2,1,0,3,4]
  return [handles[i] for i in reordering]

#-------------------------------------------------------------------------------

def TGC_comparison_plot(mrr, output_dir):
  """ Create a plot showing the correlation between the three TGCs as three
      projections.
      Assumes Gaussian uncertainties for all three TGCs.
      (That assumption does not work for lambda gamma.)
  """
  # Figure basics
  fig, axs = plt.subplots(2, 2, sharex='col', sharey='row', figsize=(10,9),
                          gridspec_kw={'hspace': 0, 'wspace': 0}, 
                          tight_layout=True)
  (ax1, ax_nouse), (ax2, ax3) = axs
  ax_nouse.axis('off')
  
  ax1.tick_params(bottom=False, top=True, left=True, right=True, 
                  labelleft=False, labeltop=True, labelright=True)
  ax2.tick_params(labelbottom=False, labelleft=False)
  ax3.tick_params(bottom=True, top=True, left=False, right=True, 
                  labeltop=True, labelright=True, labelbottom=False)

  g1_name = "Delta-g1Z"
  kg_name = "Delta-kappa_gamma"
  lg_name = "Delta-lambda_gamma"
  
  scale = 1e-3
  draw_setups(mrr, ax1, g1_name, kg_name, scale=scale, set_labels=True)
  draw_setups(mrr, ax2, g1_name, lg_name, scale=scale)
  draw_setups(mrr, ax3, kg_name, lg_name, scale=scale)
  
  ax1.text(0.0, 2.8, "$\Delta g_{1}^{Z}\, [10^{-3}]$", fontsize=30, ha='center')
  ax_nouse.text(0.0, 0.0, "$\Delta \kappa_{\gamma}\, [10^{-3}]$", fontsize=30, ha='center')
  ax3.text(3.7, 0.0, "$\Delta \lambda_{\gamma}\, [10^{-3}]$", fontsize=30, ha='center')
    
  for ax in [ax1,ax2,ax3]:
    ax.plot([0],[0], marker="X", ls="none", ms=15, color="black")

  # Create a useful legend
  handles = reorder_legend_handles(ax1)
  legend = ax1.legend(handles=handles, bbox_to_anchor=(1.4, 0.7), 
                      loc='lower left')

  # Save the plot in files
  for out_format in ["pdf","png"]:
    format_dir = "{}/{}".format(output_dir,out_format)
    IOSH.create_dir(format_dir)
    fig.savefig("{}/TGC_comp_plane.{}".format(format_dir,out_format))
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
    IORS.RunSetup("2polExt_LPcnstr", 80, 30, "constrained", "constrained"),
    IORS.RunSetup("2pol_LPcnstr", 80, 30, "constrained", "constrained"),
    IORS.RunSetup("1pol_LPcnstr", 80,  0, "constrained", "constrained"),
  ]
  unpol_run_setups = [
    IORS.RunSetup("0pol_LPcnstr",  0,  0, "constrained", "constrained"),
  ]
  muacc_setups = [
    IOMAS.MuAccSetup("MuAccFree", 0.9925, "free", "free"),
  ]
  WW_setups = [
    IOWWS.WWSetup("WWcTGCs_xs0Free_AFixd")
  ]
  
  mrr = IOMRR.MultiResultReader(fit_output_base, pol_lumi_setups, 
                                pol_run_setups, muacc_setups, 
                                WW_setups=WW_setups)
  mrr.append(IOMRR.MultiResultReader(fit_output_base, unpol_lumi_setups, 
                                     unpol_run_setups, muacc_setups, 
                                     WW_setups=WW_setups))

  # Output directories
  output_dir = "{}/plots/TGCPlaneComparison".format(output_base)

  TGC_comparison_plot(mrr, output_dir)
  
if __name__ == "__main__":
  main()