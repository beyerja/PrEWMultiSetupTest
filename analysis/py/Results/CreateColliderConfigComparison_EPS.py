from decimal import Decimal
import logging as log
import matplotlib.pyplot as plt
import numpy as np
import sys

# Local modules
sys.path.append("..") # Use the modules in the top level directory
import Analysis.ResultSummary as ARS
import IO.MultiResultReader as IOMRR
import IO.NamingConventions as IONC
import IO.SysHelp as IOSH
import Plotting.DefaultFormat as PDF
import Plotting.SetupPlotting as PSP
import Setups.DifParamSetup as IODPS
import Setups.MuAccSetup as IOMAS
import Setups.RunSetup as IORS

#-------------------------------------------------------------------------------

def draw_setups(mrr, ax, x, y_fcts):
  """ This part should be common for all physics and nuisance histograms:
      The drawing of the different setups
  """
  x_shifts, bar_width = np.linspace(-0.27,0.27,4,endpoint=True,retstep=True)
  marker_shifts = np.linspace(-bar_width/2,bar_width/2,4,endpoint=True)
  ms = 8 # marker size
  
  _x = x+x_shifts[0]
  y = y_fcts[0](mrr.get(2000, "2pol_LPcnstr", "MuAccFree", "mumu_free").result_summary())
  bar = ax.bar(_x, y, width=bar_width, align='center', zorder=2, label=r"$(80\%,30\%)$, $2$ab$^{-1}$")
  color = bar.patches[0].get_facecolor()
  y = y_fcts[0](mrr.get(2000, "2pol_Lconstr_Pfixed", "MuAccFree", "mumu_free").result_summary())
  ax.plot(_x+marker_shifts[1], y, mec="black", ls="", marker="X", ms=ms, color=color, zorder=3)#, alpha=0.3)      
  y = y_fcts[0](mrr.get(2000, "2pol_LPcnstr", "MuAccFixd", "mumu_free").result_summary())
  ax.plot(_x+marker_shifts[2], y, mec="black", ls="", marker="*", ms=ms, color=color, zorder=3)#, alpha=0.3)      

  _x = x+x_shifts[1]
  y = y_fcts[1](mrr.get(2000, "1pol_LPcnstr", "MuAccFree", "mumu_free").result_summary())
  bar = ax.bar(_x, y, width=bar_width, align='center', zorder=2, label=r"$(80\%,0\%)$, $2$ab$^{-1}$")
  color = bar.patches[0].get_facecolor()
  y = y_fcts[1](mrr.get(2000, "1pol_Lconstr_Pfixed", "MuAccFree", "mumu_free").result_summary())
  ax.plot(_x+marker_shifts[1], y, mec="black", ls="", marker="X", ms=ms, color=color, zorder=3)#, alpha=0.3)      
  y = y_fcts[1](mrr.get(2000, "1pol_LPcnstr", "MuAccFixd", "mumu_free").result_summary())
  ax.plot(_x+marker_shifts[2], y, mec="black", ls="", marker="*", ms=ms, color=color, zorder=3)#, alpha=0.3)      

  _x = x+x_shifts[2]
  y = y_fcts[2](mrr.get(2000, "0pol_LPcnstr", "MuAccFree", "mumu_AFB_k0_fixed_Ae_Af_kR").result_summary())
  bar = ax.bar(_x, y, width=bar_width, align='center', zorder=2, label=r"$(0\%,0\%)$, $2$ab$^{-1}$")
  color = bar.patches[0].get_facecolor()
  y = y_fcts[2](mrr.get(2000, "0pol_Lconstr_P0fixed", "MuAccFree", "mumu_AFB_k0_fixed_Ae_Af_kR").result_summary())
  ax.plot(_x+marker_shifts[1], y, mec="black", ls="", marker="X", ms=ms, color=color, zorder=3)#, alpha=0.3) 
  y = y_fcts[2](mrr.get(2000, "0pol_LPcnstr", "MuAccFixd", "mumu_AFB_k0_fixed_Ae_Af_kR").result_summary())
  ax.plot(_x+marker_shifts[2], y, mec="black", ls="", marker="*", ms=ms, color=color, zorder=3)#, alpha=0.3)      

  _x = x+x_shifts[3]
  y = y_fcts[3](mrr.get(10000, "0pol_LPcnstr", "MuAccFree", "mumu_AFB_k0_fixed_Ae_Af_kR").result_summary())
  bar = ax.bar(_x, y, width=bar_width, align='center', zorder=2, label=r"$(0\%,0\%)$, $10$ab$^{-1}$")#, alpha=0.15)
  color = bar.patches[0].get_facecolor()
  y = y_fcts[3](mrr.get(10000, "0pol_Lconstr_P0fixed", "MuAccFree", "mumu_AFB_k0_fixed_Ae_Af_kR").result_summary())
  ax.plot(_x+marker_shifts[1], y, mec="black", ls="", marker="X", ms=ms, color=color, zorder=3)#, alpha=0.15) 
  y = y_fcts[3](mrr.get(10000, "0pol_LPcnstr", "MuAccFixd", "mumu_AFB_k0_fixed_Ae_Af_kR").result_summary())
  ax.plot(_x+marker_shifts[2], y, mec="black", ls="", marker="*", ms=ms, color=color, zorder=3)#, alpha=0.15)      

def markers_to_legend_handles(ax):
  """ Add extra entries to legend that describe the markers for different tested 
      scenarios.
  """
  handles, labels = ax.get_legend_handles_labels()
  cross_dummy = plt.scatter([], [], color='None', ec='black', marker='X', linestyle='None', s=120, label=r'all $P$ fixed')#, alpha=0.3)
  star_dummy = plt.scatter([], [], color='None', ec='black', marker='*', linestyle='None', s=120, label=r'$\mu$ acc. fixed')#, alpha=0.3)
  handles.append(cross_dummy) 
  handles.append(star_dummy) 
  return handles
  
def make_legtext_transparent(ax):
    leg = ax.get_legend()
    # leg.texts[3].set_color("gray")
    # leg.texts[4].set_color("gray")
    # leg.texts[5].set_color("gray")

#-------------------------------------------------------------------------------

def make_fit_function(x_par_names, par_norm):
  return lambda rs: np.array([rs.fit_unc(par) if par in rs.par_names else -0.3 for par in x_par_names]) / par_norm

#-------------------------------------------------------------------------------

def difermion_par_plot(mrr, output_dir, mass_range, label, scale):
  fig = plt.figure(figsize=(15,9), tight_layout=True)
  
  x = np.arange(8)+0.5
  x_ticks = [ "$\sigma_0/\sigma_0^{SM}$", "$A_e$", "$A_{\mu}$", "$\epsilon_{\mu}$", "$A_{FB,0}^{\mu}$", "$k_L$", "$k_R$", "$k_0$" ]
  plt.xticks(x, x_ticks, size='large')
  
  plt.xlabel('$e^+e^- \\rightarrow \mu\mu$ parameters at {}'.format(label), size='large')
  plt.ylabel('Uncertainty [{:.0E}]'.format(Decimal(scale)), size='large')
  ax = plt.gca()
  ax.set_xlim(0,x[-1])
  ax.set_ylim(0,35)

  par_base_names = np.array([
   "s0_2f_mu", "Ae_2f_mu", "Af_2f_mu", "ef_2f_mu", "AFB_2f_mu", "kL_2f_mu", "kR_2f_mu", "k0_2f_mu"])
  par_names = np.array(["{}_{}".format(par,mass_range) for par in par_base_names])
  y_fct_pol = make_fit_function(par_names, scale)
  y_fct_unpol = lambda rs: y_fct_pol(rs) - 10 * np.any([par_base_names == "Ae_2f_mu",par_base_names == "Af_2f_mu",par_base_names == "kR_2f_mu"], axis=0)
  y_fcts = [ y_fct_pol, y_fct_pol, y_fct_unpol, y_fct_unpol ]

  draw_setups(mrr, ax, x, y_fcts)

  # Add markers for the tested scenarios to legend
  handles = markers_to_legend_handles(ax)
  
  legend = plt.legend(handles=handles, title="$(P_{e^{-}},P_{e^{+}})$, $L$", ncol=3, fontsize=17, bbox_to_anchor=(-0.1, 1.05), loc='lower left')
  make_legtext_transparent(ax)

  ax.set_xticks(x + 0.5, minor=True)
  ax.grid(True,which="minor",axis="x",ls='--')

  for out_format in ["pdf","png"]:
    format_dir = "{}/{}".format(output_dir,out_format)
    IOSH.create_dir(format_dir)
    fig.savefig("{}/2f_pars_{}.{}".format(format_dir,mass_range,out_format), transparent=True)
  plt.close(fig)


def nuisance_par_plot(mrr, output_dir, scale):
  fig = plt.figure(figsize=(25,9), tight_layout=True)
  
  x = np.arange(9)+0.5
  x_ticks = [ r"$L$", r"$P_{e^-}^{-}$", r"$P_{e^-}^{+}$", r"(*)$P_{e^-}^{0}$", 
              r"$P_{e^+}^{-}$", r"$P_{e^+}^{+}$", r"(*)$P_{e^+}^{0}$", 
              r"(*)$\Delta c$", r"(*)$\Delta w$" ]
  plt.xticks(x, x_ticks, size='large')
  
  plt.xlabel('Nuisance parameters', size='large')
  plt.ylabel('Rel. (*Abs.) Uncertainty [{:.0E}]'.format(Decimal(scale)), size='large')
  ax = plt.gca()
  ax.set_xlim(0,x[-1])
  ax.set_ylim(0,35)


  par_names = [ "Lumi", "ePol-", "ePol+", "ePol0", "pPol-", "pPol+", "pPol0", "MuonAcc_dCenter", "MuonAcc_dWidth" ]  
                
  par_norm_2invab  = np.array([ 2000, 0.8, 0.8, 1.0, 0.3, 0.3, 1.0, 0.1, 0.1]) * scale
  par_norm_10invab = np.array([10000, 0.8, 0.8, 1.0, 0.3, 0.3, 1.0, 0.1, 0.1]) * scale
  
  
  y_fcts = [
    make_fit_function(par_names, par_norm_2invab),
    make_fit_function(par_names, par_norm_2invab),
    make_fit_function(par_names, par_norm_2invab),
    make_fit_function(par_names, par_norm_10invab)
  ]

  draw_setups(mrr, ax, x, y_fcts)
  
  # Show the constraints
  x_constr = np.arange(7)+0.5
  y_constr = np.array([3.e-3,2.5e-3,2.5e-3,2.5e-3,2.5e-3,2.5e-3,2.5e-3]) / scale
  plt.errorbar(x_constr, y_constr, xerr=0.4, color="gold", mec="black", ls="", marker="v", ms=10, zorder=3)
  
  # Add markers for the tested scenarios and the constraints to legend
  handles = markers_to_legend_handles(ax)
  constr_marker_dummy = plt.scatter([], [], color="gold", ec="black", marker='v', linestyle='-', s=120, label=r'Constraints')
  handles.append(constr_marker_dummy) 
  
  legend = plt.legend(handles=handles, title="$(P_{e^{-}},P_{e^{+}})$, $L$", ncol=4, fontsize=17, bbox_to_anchor=(-0.02, 1.05), loc='lower left')
  make_legtext_transparent(ax)
  
  ax.set_xticks(x + 0.5, minor=True)
  ax.grid(True,which="minor",axis="x",ls='--')
  
  textstr='x10'
  ax.text(0.8, 0.15, textstr, transform=ax.transAxes, verticalalignment='top')
  ax.text(0.9, 0.25, textstr, transform=ax.transAxes, verticalalignment='top')
  
  for out_format in ["pdf","png"]:
    format_dir = "{}/{}".format(output_dir,out_format)
    IOSH.create_dir(format_dir)
    fig.savefig("{}/nuisance_pars.{}".format(format_dir,out_format), transparent=True)
  plt.close(fig)

#-------------------------------------------------------------------------------

def main():
  log.basicConfig(level=log.INFO)
  PDF.set_default_mpl_format()
  
  output_base = "../../../output"
  fit_output_base = "{}/run_outputs".format(output_base)
  
  pol_lumi_setups = [ 2000 ]
  unpol_lumi_setups = [ 2000, 10000 ]
  pol_run_setups = [
  # TODO FIX THE ANNOTATIONS
    IORS.RunSetup("2polExt_LPcnstr", 80, 30, "constrained", "constrained"),
    IORS.RunSetup("2polExt_Lconstr_Pfixed", 80, 30, "constrained", "fixed"),
    IORS.RunSetup("2polExt_Lfixed_Pconstr", 80, 30, "constrained", "fixed"),
    IORS.RunSetup("2pol_LPcnstr", 80, 30, "constrained", "constrained"),
    IORS.RunSetup("2pol_Lconstr_Pfixed", 80, 30, "constrained", "fixed"),
    IORS.RunSetup("2pol_Lfixed_Pconstr", 80, 30, "constrained", "fixed"),
    IORS.RunSetup("1pol_LPcnstr", 80,  0, "constrained", "constrained"),
    IORS.RunSetup("1pol_Lconstr_Pfixed", 80,  0, "constrained", "fixed"),
    IORS.RunSetup("1pol_LPcnstr_P0fixed", 80,  0, "constrained", "constrained, P0 fixed"),
    IORS.RunSetup("1pol_Lfixed_Pconstr", 80,  0, "constrained", "fixed")
  ]
  unpol_run_setups = [
    IORS.RunSetup("0pol_LPcnstr",  0,  0, "constrained", "constrained"),
    IORS.RunSetup("0pol_Lconstr_P0fixed",  0,  0, "constrained", "fixed"),
    IORS.RunSetup("0pol_Lfixed_P0constr",  0,  0, "constrained", "fixed")
  ]
  muacc_setups = [
    IOMAS.MuAccSetup("MuAccFree", 0.9925, "free", "free"),
    IOMAS.MuAccSetup("MuAccFixd", 0.9925, "fixed", "fixed")
  ]
  pol_difparam_setups = [
    IODPS.DifParamSetup("mumu_free",                  "free", "free", "free", "free", "free", "free")
  ]
  unpol_difparam_setups = [
    IODPS.DifParamSetup("mumu_AFB_k0_fixed_Ae_Af_kR", "free", "fixed", "fixed", "free->AFB", "free->k0", "fixed")
  ]
  
  mrr = IOMRR.MultiResultReader(fit_output_base, pol_lumi_setups, 
                                pol_run_setups, muacc_setups, 
                                pol_difparam_setups)
  mrr.append(IOMRR.MultiResultReader(fit_output_base, unpol_lumi_setups, 
                                     unpol_run_setups, muacc_setups, 
                                     unpol_difparam_setups))

  # Output directories
  output_dir = "/home/jakob/DESY/Presentations/Conferences/2021_07_29_EPS_HEP/Plots/ColliderConfigComparison/bars_all".format(output_base)

  scale = 1.e-4
  difermion_par_plot(mrr, output_dir, "81to101", "return-to-Z", scale)
  difermion_par_plot(mrr, output_dir, "180to275", r"high-$\sqrt{s*}$", scale)
  nuisance_par_plot(mrr, output_dir, scale)
  
if __name__ == "__main__":
  main()