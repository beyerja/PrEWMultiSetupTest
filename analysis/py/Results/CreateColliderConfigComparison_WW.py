from decimal import Decimal
import logging as log
import matplotlib.pyplot as plt
import numpy as np
import os
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
import Setups.WWSetup as IOWWS

#-------------------------------------------------------------------------------

def adjust_ebar(ebar, ls):
  """ Adjust the given errorbar.
  """
  ebar[-1][0].set_linestyle(ls)
  return ebar

def draw_setups(mrr, ax, x, y_fcts, draw_markers=True):
  """ This part should be common for all physics and nuisance histograms:
      The drawing of the different setups
  """
  x_shifts, bar_width = np.linspace(-0.27,0.27,5,endpoint=True,retstep=True)
  marker_shifts = np.linspace(-bar_width/2,bar_width/2,6,endpoint=True)
  ebar_shifts = np.linspace(-bar_width/2,bar_width/2,3,endpoint=True)
  ms = 8 # marker size
  
  # Errorbar's need some additional prep to look nice
  eps = 5
  zeros = np.zeros_like(x)
  eps_zeros = zeros - eps
  ebar_prep = lambda y: np.array([zeros, np.where(y >= 0, y+eps, 0)])
  ebar_width = 3
  ebar_cap = 5
  
  _x = x+x_shifts[0]
  y = y_fcts[0](mrr.get(2000, "2polExt_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
  bar = ax.bar(_x, y, width=bar_width, align='center', zorder=2, label=r"$(80/0,30/0)$, $2$ab$^{-1}$")
  color = bar.patches[0].get_facecolor()
  if draw_markers:
    y = y_fcts[0](mrr.get(2000, "2polExt_Lfixed_Pconstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
    ax.plot(_x+marker_shifts[2], y, mec="black", ls="", marker="o", ms=ms, color=color, zorder=3)      
    y = y_fcts[0](mrr.get(2000, "2polExt_Lconstr_Pfixed", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
    ax.plot(_x+marker_shifts[3], y, mec="black", ls="", marker="X", ms=ms, color=color, zorder=3)      
    y = y_fcts[0](mrr.get(2000, "2polExt_LPcnstr", "MuAccFixd", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
    ax.plot(_x+marker_shifts[4], y, mec="black", ls="", marker="*", ms=ms, color=color, zorder=3)      
    y = y_fcts[0](mrr.get(2000, "2polExt_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Fixd_AFixd").result_summary())
    ax.plot(_x+marker_shifts[1], y, mec="black", ls="", marker="^", ms=ms, color=color, zorder=3)      
  y = ebar_prep(y_fcts[0](mrr.get(2000, "2polExt_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFree").result_summary()))
  adjust_ebar(ax.errorbar(_x+ebar_shifts[1], eps_zeros, yerr=y, color=color, capsize=ebar_cap, capthick=ebar_width, elinewidth=ebar_width), ls="--")
  
  _x = x+x_shifts[1]
  y = y_fcts[1](mrr.get(2000, "2pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
  bar = ax.bar(_x, y, width=bar_width, align='center', zorder=2, label=r"$(80,30)$, $2$ab$^{-1}$")
  color = bar.patches[0].get_facecolor()
  if draw_markers:
    y = y_fcts[1](mrr.get(2000, "2pol_Lfixed_Pconstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
    ax.plot(_x+marker_shifts[2], y, mec="black", ls="", marker="o", ms=ms, color=color, zorder=3)      
    y = y_fcts[1](mrr.get(2000, "2pol_Lconstr_Pfixed", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
    ax.plot(_x+marker_shifts[3], y, mec="black", ls="", marker="X", ms=ms, color=color, zorder=3)      
    y = y_fcts[1](mrr.get(2000, "2pol_LPcnstr", "MuAccFixd", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
    ax.plot(_x+marker_shifts[4], y, mec="black", ls="", marker="*", ms=ms, color=color, zorder=3)      
    y = y_fcts[1](mrr.get(2000, "2pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Fixd_AFixd").result_summary())
    ax.plot(_x+marker_shifts[1], y, mec="black", ls="", marker="^", ms=ms, color=color, zorder=3) 
  y = ebar_prep(y_fcts[1](mrr.get(2000, "2pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFree").result_summary()))
  adjust_ebar(ax.errorbar(_x+ebar_shifts[1], eps_zeros, yerr=y, color=color, capsize=ebar_cap, capthick=ebar_width, elinewidth=ebar_width), ls="--")

  _x = x+x_shifts[2]
  y = y_fcts[2](mrr.get(2000, "1pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
  bar = ax.bar(_x, y, width=bar_width, align='center', zorder=2, label=r"$(80,0)$, $2$ab$^{-1}$")
  color = bar.patches[0].get_facecolor()
  if draw_markers:
    y = y_fcts[2](mrr.get(2000, "1pol_Lfixed_Pconstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
    ax.plot(_x+marker_shifts[2], y, mec="black", ls="", marker="o", ms=ms, color=color, zorder=3)      
    y = y_fcts[2](mrr.get(2000, "1pol_Lconstr_Pfixed", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
    ax.plot(_x+marker_shifts[3], y, mec="black", ls="", marker="X", ms=ms, color=color, zorder=3)      
    y = y_fcts[2](mrr.get(2000, "1pol_LPcnstr", "MuAccFixd", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
    ax.plot(_x+marker_shifts[4], y, mec="black", ls="", marker="*", ms=ms, color=color, zorder=3)      
    y = y_fcts[2](mrr.get(2000, "1pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Fixd_AFixd").result_summary())
    ax.plot(_x+marker_shifts[1], y, mec="black", ls="", marker="^", ms=ms, color=color, zorder=3) 
  y = ebar_prep(y_fcts[2](mrr.get(2000, "1pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFree").result_summary()))
  adjust_ebar(ax.errorbar(_x+ebar_shifts[1], eps_zeros, yerr=y, color=color, capsize=ebar_cap, capthick=ebar_width, elinewidth=ebar_width), ls="--")

  _x = x+x_shifts[3]
  y = y_fcts[3](mrr.get(2000, "0pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
  bar = ax.bar(_x, y, width=bar_width, align='center', zorder=2, label=r"$(0,0)$, $2$ab$^{-1}$")
  color = bar.patches[0].get_facecolor()
  if draw_markers:
    y = y_fcts[3](mrr.get(2000, "0pol_Lfixed_P0constr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
    ax.plot(_x+marker_shifts[2], y, mec="black", ls="", marker="o", ms=ms, color=color, zorder=3) 
    y = y_fcts[3](mrr.get(2000, "0pol_Lconstr_P0fixed", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
    ax.plot(_x+marker_shifts[3], y, mec="black", ls="", marker="X", ms=ms, color=color, zorder=3) 
    y = y_fcts[3](mrr.get(2000, "0pol_LPcnstr", "MuAccFixd", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
    ax.plot(_x+marker_shifts[4], y, mec="black", ls="", marker="*", ms=ms, color=color, zorder=3)      
    y = y_fcts[3](mrr.get(2000, "0pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Fixd_AFixd").result_summary())
    ax.plot(_x+marker_shifts[1], y, mec="black", ls="", marker="^", ms=ms, color=color, zorder=3) 
  y = ebar_prep(y_fcts[3](mrr.get(2000, "0pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFree").result_summary()))
  adjust_ebar(ax.errorbar(_x+ebar_shifts[1], eps_zeros, yerr=y, color=color, capsize=ebar_cap, capthick=ebar_width, elinewidth=ebar_width), ls="--")

  _x = x+x_shifts[4]
  y = y_fcts[4](mrr.get(10000, "0pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
  bar = ax.bar(_x, y, width=bar_width, align='center', zorder=2, label=r"$(0,0)$, $10$ab$^{-1}$")
  color = bar.patches[0].get_facecolor()
  if draw_markers:
    y = y_fcts[4](mrr.get(10000, "0pol_Lfixed_P0constr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
    ax.plot(_x+marker_shifts[2], y, mec="black", ls="", marker="o", ms=ms, color=color, zorder=3) 
    y = y_fcts[4](mrr.get(10000, "0pol_Lconstr_P0fixed", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
    ax.plot(_x+marker_shifts[3], y, mec="black", ls="", marker="X", ms=ms, color=color, zorder=3) 
    y = y_fcts[4](mrr.get(10000, "0pol_LPcnstr", "MuAccFixd", WW_name="WWcTGCs_xs0Free_AFixd").result_summary())
    ax.plot(_x+marker_shifts[4], y, mec="black", ls="", marker="*", ms=ms, color=color, zorder=3)      
    y = y_fcts[4](mrr.get(10000, "0pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Fixd_AFixd").result_summary())
    ax.plot(_x+marker_shifts[1], y, mec="black", ls="", marker="^", ms=ms, color=color, zorder=3) 
  y = ebar_prep(y_fcts[4](mrr.get(10000, "0pol_LPcnstr", "MuAccFree", WW_name="WWcTGCs_xs0Free_AFree").result_summary()))
  adjust_ebar(ax.errorbar(_x+ebar_shifts[1], eps_zeros, yerr=y, color=color, capsize=ebar_cap, capthick=ebar_width, elinewidth=ebar_width), ls="--")

def markers_to_legend_handles(ax, draw_markers=True):
  """ Add extra entries to legend that describe the markers for different tested 
      scenarios.
  """
  handles, labels = ax.get_legend_handles_labels()
  
  if draw_markers:
    dot_dummy = plt.scatter([], [], color='None', ec='black', marker='o', linestyle='None', s=120, label=r'$L$ fixed')
    star_dummy = plt.scatter([], [], color='None', ec='black', marker='*', linestyle='None', s=120, label=r'$\mu$ acc. fixed')
    cross_dummy = plt.scatter([], [], color='None', ec='black', marker='X', linestyle='None', s=120, label=r'all $P$ fixed')
    triangle_dummy = plt.scatter([], [], color='None', ec='black', marker='^', linestyle='None', s=120, label=r'$\sigma_0$ fixed')
  
  ebar_width = 3
  ebar_d_dummy = ax.plot([], [], color='black', lw=ebar_width, ls="--", label="$A_{LR}$ free")
  
  if draw_markers:
    handles.append(triangle_dummy) 
    
  handles.append(ebar_d_dummy[0]) 
  
  if draw_markers:
    handles.append(dot_dummy) 
    handles.append(cross_dummy) 
    handles.append(star_dummy) 
  
  return handles

#-------------------------------------------------------------------------------

def make_fit_function(x_par_names, par_norm):
  # Needs some weird special treatment to make sure xs0 marker is drawn when fix
  return lambda rs: (np.array([rs.fit_unc(par) if par in rs.par_names 
                                              else -0.3 
                              for par in x_par_names]) + \
                     np.array([0.3 if (par in ["ScaleTotChiXS_WW_muminus", "ScaleTotChiXS_WW_muplus"] and par not in rs.par_names) 
                                   else 0
                              for par in x_par_names])) / par_norm 

#-------------------------------------------------------------------------------

def TGC_par_plot(mrr, output_dir, scale, set_ylim=True):
  fig = plt.figure(figsize=(10,7.5), tight_layout=True)
  
  x = np.arange(3)+0.5
  x_ticks = [ "$g_{1}^{Z}$", "$\kappa_{\gamma}$", "$\lambda_{\gamma}$" ]
  plt.xticks(x, x_ticks, size='large')
  
  plt.xlabel('Triple Gauge Couplings', size='large')
  plt.ylabel('Abs. uncertainty [{:.0E}]'.format(Decimal(scale)), size='large')
  ax = plt.gca()
  ax.set_xlim(0,x[-1])
  
  if set_ylim:
    ax.set_ylim(0,35)

  par_names = np.array([ 
    "Delta-g1Z", "Delta-kappa_gamma", "Delta-lambda_gamma" ])
  y_fct = make_fit_function(par_names, scale)
  y_fcts = [y_fct for i in range(5)]

  draw_setups(mrr, ax, x, y_fcts, draw_markers=set_ylim)
  
  ax.set_ylim(0,ax.get_ylim()[1])

  # Add markers for the tested scenarios to legend
  handles = markers_to_legend_handles(ax, draw_markers=set_ylim)
  
  ncol = 2 if set_ylim else 1
  legend = plt.legend(handles=handles, title="$(P_{e^{-}}[\%],P_{e^{+}}[\%])$, $L$", ncol=ncol, fontsize=17)
  ax.set_xticks(x + 0.5, minor=True)
  ax.grid(True,which="minor",axis="x",ls='--')

  for out_format in ["pdf","png"]:
    format_dir = "{}/{}".format(output_dir,out_format)
    IOSH.create_dir(format_dir)
    ylim_str = "" if set_ylim else "_noYLim"
    fig.savefig("{}/TGC_pars{}.{}".format(format_dir,ylim_str,out_format), transparent=True)
  plt.close(fig)

def WW_par_plot(mrr, output_dir, scale):
  fig = plt.figure(figsize=(12,7.5), tight_layout=True)
  
  x = np.arange(4)+0.5
  x_ticks = [ "$\sigma_0/\sigma_0^{SM}(W^{-})$", "$\sigma_0/\sigma_0^{SM}(W^{+})$", "$A_{LR} (W^{-})$", "$A_{LR} (W^{+})$" ]
  plt.xticks(x, x_ticks, size='large')
  
  plt.xlabel('$WW$ cross section parameters', size='large')
  plt.ylabel('Abs. uncertainty [{:.0E}]'.format(Decimal(scale)), size='large')
  ax = plt.gca()
  ax.set_xlim(0,x[-1])
  ax.set_ylim(0,60)

  par_names = np.array([ "ScaleTotChiXS_WW_muminus", "ScaleTotChiXS_WW_muplus", 
                         "DeltaA_WW_muminus", "DeltaA_WW_muplus" ])
  y_fct = make_fit_function(par_names, scale)
  y_fcts = [y_fct for i in range(5)]

  draw_setups(mrr, ax, x, y_fcts)

  # Add markers for the tested scenarios to legend
  handles = markers_to_legend_handles(ax)
  
  legend = plt.legend(handles=handles, title="$(P_{e^{-}}[\%],P_{e^{+}}[\%])$, $L$", ncol=2, fontsize=17)

  ax.set_xticks(x + 0.5, minor=True)
  ax.grid(True,which="minor",axis="x",ls='--')

  for out_format in ["pdf","png"]:
    format_dir = "{}/{}".format(output_dir,out_format)
    IOSH.create_dir(format_dir)
    fig.savefig("{}/WW_pars.{}".format(format_dir,out_format), transparent=True)
  plt.close(fig)

def nuisance_par_plot(mrr, output_dir, scale):
  fig = plt.figure(figsize=(20,7.5), tight_layout=True)
  
  x = np.arange(9)+0.5
  x_ticks = [ r"$L$", r"$P_{e^-}^{-}$", r"$P_{e^-}^{+}$", r"(*)$P_{e^-}^{0}$", 
              r"$P_{e^+}^{-}$", r"$P_{e^+}^{+}$", r"(*)$P_{e^+}^{0}$", 
              r"(*)$\Delta c$", r"(*)$\Delta w$" ]
  plt.xticks(x, x_ticks, size='large')
  
  plt.xlabel('Nuisance parameters', size='large')
  plt.ylabel('Rel. (*Abs.) uncertainty [{:.0E}]'.format(Decimal(scale)), size='large')
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
  
  legend = plt.legend(handles=handles, title="$(P_{e^{-}}[\%],P_{e^{+}}[\%])$, $L$", ncol=6, fontsize=17, loc="upper center")
  
  ax.set_xticks(x + 0.5, minor=True)
  ax.grid(True,which="minor",axis="x",ls='--')
  
  textstr='x10'
  ax.text(0.8, 0.25, textstr, transform=ax.transAxes, verticalalignment='top')
  ax.text(0.9, 0.4, textstr, transform=ax.transAxes, verticalalignment='top')
  
  for out_format in ["pdf","png"]:
    format_dir = "{}/{}".format(output_dir,out_format)
    IOSH.create_dir(format_dir)
    fig.savefig("{}/nuisance_pars.{}".format(format_dir,out_format), transparent=True)
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
    IORS.RunSetup("2polExt_Lfixed_Pconstr"),
    IORS.RunSetup("2pol_LPcnstr"),
    IORS.RunSetup("2pol_Lconstr_Pfixed"),
    IORS.RunSetup("2pol_Lfixed_Pconstr"),
    IORS.RunSetup("1pol_LPcnstr"),
    IORS.RunSetup("1pol_Lconstr_Pfixed"),
    IORS.RunSetup("1pol_Lfixed_Pconstr"),
  ]
  unpol_run_setups = [
    IORS.RunSetup("0pol_LPcnstr"),
    IORS.RunSetup("0pol_Lconstr_P0fixed"),
    IORS.RunSetup("0pol_Lfixed_P0constr")
  ]
  muacc_setups = [
    IOMAS.MuAccSetup("MuAccFree"),
    IOMAS.MuAccSetup("MuAccFixd")
  ]
  WW_setups = [
    IOWWS.WWSetup("WWcTGCs_xs0Free_AFree"),
    IOWWS.WWSetup("WWcTGCs_xs0Free_AFixd"),
    IOWWS.WWSetup("WWcTGCs_xs0Fixd_AFixd")
  ]
  
  mrr = IOMRR.MultiResultReader(fit_output_base, pol_lumi_setups, 
                                pol_run_setups, muacc_setups, 
                                WW_setups=WW_setups)
  mrr.append(IOMRR.MultiResultReader(fit_output_base, unpol_lumi_setups, 
                                     unpol_run_setups, muacc_setups, 
                                     WW_setups=WW_setups))

  # Output directories
  output_dir = "{}/plots/ColliderConfigComparison/WW".format(output_base)

  scale = 1.e-4
  TGC_par_plot(mrr, output_dir, scale)
  TGC_par_plot(mrr, output_dir, scale, set_ylim=False)
  WW_par_plot(mrr, output_dir, scale)
  nuisance_par_plot(mrr, output_dir, scale)
  
if __name__ == "__main__":
  main()
