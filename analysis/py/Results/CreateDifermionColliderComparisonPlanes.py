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
import Setups.DifParamSetup as IODPS
import Setups.MuAccSetup as IOMAS
import Setups.RunSetup as IORS

#-------------------------------------------------------------------------------

# True values of the difermion parameters
truth_vals = {
  "return-to-Z": {
    "Ae": 0.21360014,
    "Af": 0.20281099,
    "ef": 0.01580906,
    "k0": 0.07471141,
    "dk": 0.00059199,
  },
  r"high-$\sqrt{s*}$": {
    "Ae" : 0.11251847,
    "Af" : 0.03217479,
    "ef" : 1.42594481,
    "k0" : 0.00033356,
    "dk" : 0.00031470,
  }
}

#-------------------------------------------------------------------------------

def Af_fromAFB(AFB, Ae, ef):
  """ Calculate Af from AFB for given Ae and epsilon_f.
  """
  return (AFB - ef) / (2 * Ae)
  
#-------------------------------------------------------------------------------

def draw_ellipse(ax, rs, Ae_name, Af_name, mass_label, **kwargs):
  """ Draw the Ae, Af covariance matrix ellipse for a given result summary.
  """
  i_Ae = rs.par_index(Ae_name)
  i_Af = rs.par_index(Af_name)
  full_cov = rs.cov_mat_avg
  AeAf_cov = np.array([[full_cov[i_Ae,i_Ae],full_cov[i_Af,i_Ae]],
                       [full_cov[i_Ae,i_Af],full_cov[i_Af,i_Af]]])
                       
  mean_Ae = truth_vals[mass_label]["Ae"]
  mean_Af = truth_vals[mass_label]["Af"]
  PS.confidence_ellipse(AeAf_cov, mean_Ae, mean_Af, ax, n_std=1.0, **kwargs)

def draw_FCCee_TeraZ(ax, scale=1.0, **kwargs):
  """ Draw the expected result for the FCCee Tera-Z.
  
      AFB(mumu) ref: https://arxiv.org/pdf/1601.03849.pdf
      Ae ref:
        FCC-ee # Z-pole tautau events: 
          https://link.springer.com/article/10.1140/epjp/s13360-021-01894-y
        LEP # Z-pol tautau events & Ae precision from tau polarisation:
          https://arxiv.org/abs/hep-ex/0312023
      
      Assumes an AFB measurement in the mumu channel of 4 * 10^-6,
      and an independent measurement of Ae from tau polarisation.
      For the Ae uncertainty I take the LEP uncertainty on Ae from tau
      polarisation (~0.005) and devide it by the increased statistics (10^7 more
      Z events at FCC-ee Tera-Z).
  """
  unc_AFB = 5.e-6
  
  N_Ztatau_LEP = 1724e3 / 3
  N_Ztatau_FCCee = 1.7e11
  unc_Ae = 5.e-3 / np.sqrt( N_Ztatau_FCCee / N_Ztatau_LEP ) # ~ 9e-6
  
  Ae = truth_vals["return-to-Z"]["Ae"]
  Af = truth_vals["return-to-Z"]["Af"]
  ef = truth_vals["return-to-Z"]["ef"]
  AFB = ef - 2 * Ae * Af
  
  # Transform the covariance matrix from AFB:Ae to Amu:Ae
  cov_AeAFB = np.array([[unc_Ae**2, 0.],
                        [0.,        unc_AFB**2]])
  transf_mat = np.array([[1.,         0.],
                         [-1./(2.*Ae**2) * (AFB - ef), 1./(2.*Ae)]])
  cov_AeAf = np.matmul(np.matmul(transf_mat, cov_AeAFB), transf_mat.T) 
  cov_AeAf_scaled = cov_AeAf * scale**2
  
  # print(np.sqrt(cov_AeAf))
  # print(cov_AeAf[0][1] / np.sqrt(cov_AeAf[0][0]) / np.sqrt(cov_AeAf[1][1]))
  
  PS.confidence_ellipse(cov_AeAf_scaled, Ae, Af, ax, n_std=1.0, **kwargs)

def draw_ILC_GigaZ(ax, scale=1.0, **kwargs):
  """ Draw the expected result for the ILC Giga-Z.
      Ref: https://arxiv.org/pdf/1905.00220.pdf
      Assumes that the A_e and A_mu measurements are uncorrelated (which is 
      likely).
  """
  unc_Ae = 1.e-4
  unc_Amu = 3.e-4
  
  Ae = truth_vals["return-to-Z"]["Ae"]
  Af = truth_vals["return-to-Z"]["Af"]
  
  # Transform the covariance matrix from AFB:Ae to Amu:Ae
  cov_AeAf = np.array([[unc_Ae**2, 0.],
                       [0.,        unc_Amu**2]])
  cov_AeAf_scaled = cov_AeAf * scale**2
  
  # print(np.sqrt(cov_AeAf))
  # print(cov_AeAf[0][1] / np.sqrt(cov_AeAf[0][0]) / np.sqrt(cov_AeAf[1][1]))
  
  PS.confidence_ellipse(cov_AeAf_scaled, Ae, Af, ax, n_std=1.0, **kwargs)

def draw_unpol_range(ax, rs, AFB_name, mass_label, **kwargs):
  """ Draw the range that the unpolarised collider can constrain in the Ae/Af
      plane, assuming epsilon_f to be known perfectly. 
  """
  
  # Determine the upper and lower Ae/Af bands
  i_AFB = rs.par_index(AFB_name)
  
  unc_AFB = rs.unc_vec_avg[i_AFB]
  val_AFB = rs.par_avg[i_AFB]
  AFB_low = val_AFB - unc_AFB 
  AFB_up = val_AFB + unc_AFB 

  Ae_min, Ae_max = ax.get_xlim()
  Ae_vals = np.linspace(Ae_min, Ae_max, 500)
  
  ef = truth_vals[mass_label]["ef"]
  Af_low = Af_fromAFB(AFB_low, Ae_vals, ef)
  Af_up = Af_fromAFB(AFB_up, Ae_vals, ef)
  
  # Draw the two bands
  p_low = ax.plot(Ae_vals, Af_low, **kwargs)
  kwargs['color'] = p_low[0].get_color()
  del kwargs['label']
  p_up = ax.plot(Ae_vals, Af_up, **kwargs)
  
  # Reset the x limits
  ax.set_xlim(Ae_min, Ae_max)
  
def adjust_ebar(ebar, ls):
  """ Adjust the given errorbar linestyle.
  """
  ebar[-1][0].set_linestyle(ls)
  return ebar
  
def draw_unpol_opt(ax, rs, AFB_name, mass_label, set_axlims=False, **kwargs):
  """ Draw optimistic errorbars for the unpolarised scenarios assuming Ae or Af 
      perfectly known / fixed.
  """
  i_AFB = rs.par_index(AFB_name)
  unc_AFB = rs.unc_vec_avg[i_AFB]
  
  Ae = truth_vals[mass_label]["Ae"]
  Af = truth_vals[mass_label]["Af"]
  
  # Simple Gaussian error propagation
  unc_Ae = unc_AFB / (2 * Af)
  unc_Af = unc_AFB / (2 * Ae)
  
  xlims = ax.get_xlim()
  ylims = ax.get_ylim()
  if set_axlims:
    xlims = [Ae - 1.2 * unc_Ae, Ae + 1.2 * unc_Ae]
    ylims = [Af - 1.2 * unc_Af, Af + 1.2 * unc_Af]
  
  labels=[None, None]
  if 'label' in kwargs:
    base_label = kwargs['label']
    labels = [
      "{}, {{$A_{{\mu}},\epsilon_{{\mu}}$}} fixed".format(base_label),
      "{}, {{$A_e,\epsilon_{{\mu}}$}} fixed".format(base_label)
    ]
    del kwargs['label']
  
  # adjust_ebar(ax.errorbar([Ae],[Af],xerr=unc_Ae,label=labels[0],**kwargs),ls='dotted')
  adjust_ebar(ax.errorbar([Ae],[Af],yerr=unc_Af,label=labels[1],**kwargs),ls=':')
  
  ax.set_xlim(xlims)
  ax.set_ylim(ylims)

def draw_setups(mrr, ax, Ae_name, Af_name, AFB_name, mass_label, draw_colliders=False):
  """ Draw all the different visualisations for the Ae-Af uncertainties from the 
      different collider setups.
  """ 
  # Recover all result summaries 
  rs_2polExt = mrr.get(2000, "2polExt_LPcnstr", "MuAccFree", "mumu_free").result_summary()
  rs_2pol = mrr.get(2000, "2pol_LPcnstr", "MuAccFree", "mumu_free").result_summary()
  rs_1pol = mrr.get(2000, "1pol_LPcnstr", "MuAccFree", "mumu_free").result_summary()
  rs_0pol_2 = mrr.get(2000, "0pol_LPcnstr", "MuAccFree", "mumu_AFB_k0_fixed_Ae_Af_dk").result_summary()
  rs_0pol_10 = mrr.get(10000, "0pol_LPcnstr", "MuAccFree", "mumu_AFB_k0_fixed_Ae_Af_dk").result_summary()

  # Get the colors of the color cycle (to get manual control over them)
  colors =  plt.rcParams['axes.prop_cycle'].by_key()['color']
  
  # Draw the polarised setups as ellipses
  draw_ellipse(ax, rs_1pol, Ae_name, Af_name, mass_label, ls="-", lw=5.0, edgecolor=colors[2], facecolor='none', label="(80,0), 2ab$^{-1}$", zorder=2)
  draw_ellipse(ax, rs_2pol, Ae_name, Af_name, mass_label, ls="-", lw=5.0, edgecolor=colors[1], facecolor='none', label="(80,30), 2ab$^{-1}$", zorder=2)
  draw_ellipse(ax, rs_2polExt, Ae_name, Af_name, mass_label, ls="-", lw=4.0, edgecolor=colors[0], facecolor='none', label="(80/0,30/0), 2ab$^{-1}$", zorder=2)

  # Draw optimistic and less optimistic limits for the unpolarised setups
  draw_unpol_opt(ax, rs_0pol_2, AFB_name, mass_label, color=colors[3], lw=5, capsize=15, capthick=5, alpha=0.9, label="(0,0), 2ab$^{-1}$", ls='none', set_axlims=True)
  draw_unpol_opt(ax, rs_0pol_10, AFB_name, mass_label, color=colors[4], lw=5, capsize=15, capthick=5, alpha=0.9, label="(0,0), 10ab$^{-1}$", ls='none')
  
  draw_unpol_range(ax, rs_0pol_2, AFB_name, mass_label, lw=5.0, color=colors[3], label="(0,0), 2ab$^{-1}$, $\epsilon_{\mu}$ fixed", zorder=1)
  draw_unpol_range(ax, rs_0pol_10, AFB_name, mass_label, lw=5.0, color=colors[4], label="(0,0), 10ab$^{-1}$, $\epsilon_{\mu}$ fixed", zorder=1)
  
  if (mass_label == "return-to-Z") and draw_colliders:
    scale_FCCee = 100.
    arxiv_FCCee = "1601.03849"
    draw_FCCee_TeraZ(ax, scale=scale_FCCee, label="FCCee (Tera-Z), $\epsilon_{{\mu}}$ fixed\nScaled $\\bf{{x{}}}$\narXiv:{}".format(int(scale_FCCee),arxiv_FCCee), zorder=3, ls="--", lw=5.0, edgecolor=colors[5], facecolor='none')
    scale_ILC = 5.
    arxiv_ILC = "1905.00220"
    draw_ILC_GigaZ(ax, scale=scale_ILC, label="ILC (Giga-Z)\nScaled $\\bf{{x{}}}$\narXiv:{}".format(int(scale_ILC),arxiv_ILC), zorder=3, ls="--", lw=5.0, edgecolor=colors[6], facecolor='none')
  else:
    ax.plot([],[],color="white",label="\n\n",zorder=3)
    ax.plot([],[],color="white",label="\n\n",zorder=3)
  
def draw_true_point(ax, mass_label, **kwargs):
  """ Mark the true Ae-Af point on the plot.
  """
  if mass_label in truth_vals:
    ax.plot([truth_vals[mass_label]["Ae"]],[truth_vals[mass_label]["Af"]], 
            **kwargs)
  else:
    raise Exception("Unknown label {}".format(mass_label))

#-------------------------------------------------------------------------------

def reorder_legend_handles(ax, draw_colliders=False):
  """ Reorder the legend handles to make the legend look more orderly.
  """
  handles, _ = ax.get_legend_handles_labels()
  if (len(handles) == 10) and draw_colliders:
    reordering = [3,4,5,2,0,8,6,1,9,7]
  elif (len(handles) == 10) and not draw_colliders:
    reordering = [5,6,7,4,0,8,3,1,9,2]
  elif (len(handles) == 8):
    reordering = [3,4,5,0,6,2,1,7]
  else:
    raise Exception("Not prepared for {} labels.".format(len(handles)))
    
  return [handles[i] for i in reordering]

#-------------------------------------------------------------------------------

def AeAf_comparison_plot(mrr, output_dir, mass_range, label, draw_colliders=False):
  """ Create the Ae - Af plane comparison plot for the different collider 
      setups.
  """
  # Figure basics
  fig = plt.figure(figsize=(12.5,12.5), tight_layout=True)
  ax = plt.gca()
  ax.set_xlabel("$A_e$")
  ax.set_ylabel("$A_{\mu}$")

  # Get the parameter names
  par_base_names = np.array([
   "s0_2f_mu", "Ae_2f_mu", "Af_2f_mu", "ef_2f_mu", "AFB_2f_mu", "k0_2f_mu", "dk_2f_mu"])
  par_names = np.array(["{}_{}".format(par,mass_range) for par in par_base_names])
  s0_name, Ae_name, Af_name, ef_name, AFB_name, k0_name, dk_name = par_names 

  # Draw all the necessary lines
  draw_setups(mrr, ax, Ae_name, Af_name, AFB_name, label, draw_colliders)
  draw_true_point(ax, label, marker="X", ls="none", ms=15, color="black", label="Truth")

  # Create a useful legend
  handles = reorder_legend_handles(ax, draw_colliders)
  legend = plt.legend(handles=handles, ncol=3, title="$e^+e^-\\rightarrow\mu^+\mu^-$ ({}) - $(P_{{e^-}}[\%],P_{{e^+}}[\%])$, $L$".format(label), fontsize=17, title_fontsize=17, bbox_to_anchor=(-0.18, 1.02), loc='lower left')

  # Save the plot in files
  for out_format in ["pdf","png"]:
    format_dir = "{}/{}".format(output_dir,out_format)
    IOSH.create_dir(format_dir)
    collider_str = "_wColliders" if draw_colliders else ""
    fig.savefig("{}/2f_pars_{}{}.{}".format(format_dir,mass_range,collider_str,out_format), transparent=True)
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
  pol_difparam_setups = [
    IODPS.DifParamSetup("mumu_free",                  "free", "free", "free", "free", "free", "free")
  ]
  unpol_difparam_setups = [
    IODPS.DifParamSetup("mumu_AFB_k0_fixed_Ae_Af_dk", "free", "fixed", "fixed", "free->AFB", "free->k0", "fixed")
  ]
  
  mrr = IOMRR.MultiResultReader(fit_output_base, pol_lumi_setups, 
                                pol_run_setups, muacc_setups, 
                                pol_difparam_setups)
  mrr.append(IOMRR.MultiResultReader(fit_output_base, unpol_lumi_setups, 
                                     unpol_run_setups, muacc_setups, 
                                     unpol_difparam_setups))

  # Output directories
  output_dir = "{}/plots/DifermionPlaneComparison".format(output_base)

  AeAf_comparison_plot(mrr, output_dir, "81to101", "return-to-Z")
  AeAf_comparison_plot(mrr, output_dir, "81to101", "return-to-Z", draw_colliders=True)
  AeAf_comparison_plot(mrr, output_dir, "180to275", r"high-$\sqrt{s*}$")
  
if __name__ == "__main__":
  main()