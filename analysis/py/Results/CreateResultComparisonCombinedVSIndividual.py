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
import Setups.DifParamSetup as IODPS
import Setups.MuAccSetup as IOMAS
import Setups.RunSetup as IORS
import Setups.WWSetup as IOWWS

#-------------------------------------------------------------------------------

def get_ratios(par_names, rs_comb, rs_indv):
  """ Get the combined/individual fit uncertainty ratios for all parameters 
      (if they're available).
  """
  return np.array([rs_comb.fit_unc(par)/rs_indv.fit_unc(par) 
                    if par in rs_indv.par_names 
                   else -0.3 
                   for par in par_names ]) 

def draw_ratio(ax, x, par_names, rs_comb, rs_indv, **kwargs):
  """ Draw the uncertainty ratio combined / individual for the given parameters.
  """
  y = get_ratios(par_names, rs_comb, rs_indv)
  ax.plot(x, y, **kwargs)

def plot_setups(ax, rs_dict, indv_setup, par_names, x_ticklabels=None):
  """ Plot the ratios for the four collider scenarios.
  """
  x = np.arange(len(par_names))+0.5
  x_shifts, x_width = np.linspace(-0.27,0.27,5,endpoint=True,retstep=True)
  
  if x_ticklabels:
    plt.sca(ax)
    plt.xticks(x, x_ticklabels, size='large')
    ax.set_xticks(x + 0.5, minor=True)

  colors =  plt.rcParams['axes.prop_cycle'].by_key()['color']
  common_kwargs = { "ls": "", "ms": 12 }
  if indv_setup == "4f":
    colors = colors[4:]
    common_kwargs["fillstyle"] ="none"
    common_kwargs["mew"] = 3

  draw_ratio(ax, x+x_shifts[0], par_names, rs_dict["2polExt_comb"], rs_dict["2polExt_"+indv_setup], color=colors[0], marker="^", **common_kwargs)
  draw_ratio(ax, x+x_shifts[1], par_names, rs_dict["2pol_comb"], rs_dict["2pol_"+indv_setup], color=colors[1], marker="v", **common_kwargs)
  draw_ratio(ax, x+x_shifts[2], par_names, rs_dict["1pol_comb"], rs_dict["1pol_"+indv_setup], color=colors[2], marker="o", **common_kwargs)
  draw_ratio(ax, x+x_shifts[3], par_names, rs_dict["0pol_comb"], rs_dict["0pol_"+indv_setup], color=colors[3], marker="s", **common_kwargs)
  ax.set_xlim(0,x[-1]+0.5)

def plot_2f(ax, rs_dict, mass_range):
  par_base_names = np.array([
   "s0_2f_mu", "Ae_2f_mu", "Af_2f_mu", "ef_2f_mu", "AFB_2f_mu", "k0_2f_mu", "dk_2f_mu"])
  par_names = np.array(["{}_{}".format(par,mass_range) for par in par_base_names])
  x_ticks = [ "$\sigma_0/\sigma_0^{SM}$", "$A_e$", "$A_{\mu}$", "$\epsilon_{\mu}$", "$A_{FB,0}^{\mu}$", "$k_0$", "$\Delta k$" ]
  
  plot_setups(ax, rs_dict, "2f", par_names, x_ticks)
  
def plot_TGC(ax, rs_dict):
  par_names = np.array([ 
    "Delta-g1Z", "Delta-kappa_gamma", "Delta-lambda_gamma" ])
  x_ticks = [ "$g_{1}^{Z}$", "$\kappa_{\gamma}$", "$\lambda_{\gamma}$" ]

  plot_setups(ax, rs_dict, "4f", par_names, x_ticks)
  
def plot_WWpars(ax, rs_dict):
  par_names = np.array(["ScaleTotChiXS_WW_muminus", "ScaleTotChiXS_WW_muplus"])
  x_ticks = [ "$\sigma_0/\sigma_0^{SM}(W^{-})$", "$\sigma_0/\sigma_0^{SM}(W^{+})$" ]
  
  plot_setups(ax, rs_dict, "4f", par_names, x_ticks)
  
def plot_nuisancepars(ax, rs_dict):
  par_names = [ "Lumi", "ePol-", "ePol+", "ePol0", "pPol-", "pPol+", "pPol0", "MuonAcc_dCenter", "MuonAcc_dWidth" ]
  x_ticks = [ r"$L$", r"$P_{e^-}^{-}$", r"$P_{e^-}^{+}$", r"$P_{e^-}^{0}$", 
              r"$P_{e^+}^{-}$", r"$P_{e^+}^{+}$", r"$P_{e^+}^{0}$", 
              r"$\Delta c$", r"$\Delta w$" ]
  
  plot_setups(ax, rs_dict, "2f", par_names, x_ticks)
  plot_setups(ax, rs_dict, "4f", par_names)

def markers_to_legend_handles(ax, indv_setup):
  """ Create the legend labels.
  """
  handles, labels = ax.get_legend_handles_labels()

  colors =  plt.rcParams['axes.prop_cycle'].by_key()['color']
  common_kwargs = { "ls": "", "ms": 12 }
  if indv_setup == "4f":
    colors = colors[4:]
    common_kwargs["fillstyle"] ="none"
    common_kwargs["mew"] = 3

  handles.append( ax.plot([],[], label="$(80/0,30/0)$", color=colors[0], marker="^", **common_kwargs)[0] )
  handles.append( ax.plot([],[], label="$(80,30)$", color=colors[1], marker="v", **common_kwargs)[0] )
  handles.append( ax.plot([],[], label="$(80,0)$", color=colors[2], marker="o", **common_kwargs)[0] )
  handles.append( ax.plot([],[], label="$(0,0)$", color=colors[3], marker="s", **common_kwargs)[0] )
  return handles

def plot_ratios(rs_dict, output_dir):
  """ Create the ratio plot.
  """
  fig = plt.figure(figsize=(18, 14), tight_layout=True)
  ax1 = fig.add_subplot(3,2,1)
  ax2 = fig.add_subplot(3,2,2)
  ax3 = fig.add_subplot(3,2,3)
  ax4 = fig.add_subplot(3,2,4)
  ax5 = fig.add_subplot(3,1,3)
  all_ax = [ax1, ax2, ax3, ax4, ax5]
  
  plot_2f(ax1, rs_dict, "81to101")
  plot_2f(ax2, rs_dict, "180to275")
  plot_TGC(ax3, rs_dict)
  plot_WWpars(ax4, rs_dict)
  plot_nuisancepars(ax5, rs_dict)
  
  ax1.set_xlabel('$e^+e^- \\rightarrow \mu\mu$ parameters at return-to-Z', size='large')
  ax2.set_xlabel('$e^+e^- \\rightarrow \mu\mu$ parameters at high-$\sqrt{s*}$', size='large')
  ax3.set_xlabel('Triple Gauge Couplings', size='large')
  ax4.set_xlabel('$WW$ cross section parameters', size='large')
  ax5.set_xlabel('Nuisance parameters', size='large')
  fig.supylabel("Combined fit unc. / Individual fit unc.")
  
  handles_2f = markers_to_legend_handles(ax2, "2f")
  handles_4f = markers_to_legend_handles(ax4, "4f")
  
  ax2.legend(handles=handles_2f, ncol=2, fontsize=25, title_fontsize=25, title="Ratio to $\mu\mu$-only")
  ax4.legend(handles=handles_4f, ncol=2, fontsize=25, title_fontsize=25, title="Ratio to $\mu\\nu qq$-only")
  
  for ax in all_ax:
    ax.plot(ax.get_xlim(),[1,1],color="black",zorder=1)
    ax.grid(True,which="minor",axis="x",ls='--')
    ax.set_ylim(0.9, 1.005)
    ax.set_yticks([0.9,0.95,1.0])
  ax5.set_ylim(0, 1.05)
  ax5.set_yticks([0,0.5,1.0])
  
  for out_format in ["pdf","png"]:
    format_dir = "{}/{}".format(output_dir,out_format)
    IOSH.create_dir(format_dir)
    fig.savefig("{}/ratios.{}".format(format_dir,out_format), transparent=True)
  plt.close(fig)

def get_relevant_results(mrr):
  """ Get a dictionary of the relevant results from the MultiResultReader.
  """
  return {
    "2polExt_comb": mrr.get(2000, "2polExt_LPcnstr", "MuAccFree", difparam_name="mumu_free", WW_name="WWcTGCs_xs0Free_AFixd").result_summary(),
    "2pol_comb": mrr.get(2000, "2pol_LPcnstr", "MuAccFree", difparam_name="mumu_free", WW_name="WWcTGCs_xs0Free_AFixd").result_summary(),
    "1pol_comb": mrr.get(2000, "1pol_LPcnstr", "MuAccFree", difparam_name="mumu_free", WW_name="WWcTGCs_xs0Free_AFixd").result_summary(),
    "0pol_comb": mrr.get(2000, "0pol_LPcnstr", "MuAccFree", difparam_name="mumu_unpol", WW_name="WWcTGCs_xs0Free_AFixd").result_summary(),
    # 
    "2polExt_2f": mrr.get(2000, "2polExt_LPcnstr", "MuAccFree", difparam_name="mumu_free").result_summary(),
    "2pol_2f": mrr.get(2000, "2pol_LPcnstr", "MuAccFree", difparam_name="mumu_free").result_summary(),
    "1pol_2f": mrr.get(2000, "1pol_LPcnstr", "MuAccFree", difparam_name="mumu_free").result_summary(),
    "0pol_2f": mrr.get(2000, "0pol_LPcnstr", "MuAccFree", difparam_name="mumu_unpol").result_summary(),
    # 
    "2polExt_4f": mrr.get(2000, "2polExt_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary(),
    "2pol_4f": mrr.get(2000, "2pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary(),
    "1pol_4f": mrr.get(2000, "1pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary(),
    "0pol_4f": mrr.get(2000, "0pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary(),
  }
  
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
    IORS.RunSetup("0pol_LPcnstr"),
  ]
  muacc_setups = [
    IOMAS.MuAccSetup("MuAccFree"),
  ]
  pol_difparam_setups = [
    IODPS.DifParamSetup("mumu_free"),
    IODPS.DifParamSetup()
  ]
  unpol_difparam_setups = [
    IODPS.DifParamSetup("mumu_unpol"),
    IODPS.DifParamSetup()
  ]
  WW_setups = [
    IOWWS.WWSetup("WWcTGCs_xs0Free_AFixd"),
    IOWWS.WWSetup()
  ]
    
  mrr = IOMRR.MultiResultReader(fit_output_base, lumi_setups, 
                                pol_run_setups, muacc_setups, 
                                difparam_setups=pol_difparam_setups, 
                                WW_setups=WW_setups)
  mrr.append(IOMRR.MultiResultReader(fit_output_base, lumi_setups, 
                                     unpol_run_setups, muacc_setups, 
                                     difparam_setups=unpol_difparam_setups, 
                                     WW_setups=WW_setups))

  rs_dict = get_relevant_results(mrr)

  # Output directories
  output_dir = "{}/plots/CombinedVSIndividual".format(output_base)

  plot_ratios(rs_dict, output_dir)
  
if __name__ == "__main__":
  main()
