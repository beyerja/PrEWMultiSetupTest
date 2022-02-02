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
    "sigma0": 6621.4,
    "Ae": 0.21360014,
    "Af": 0.20281099,
    "ef": 0.01580906,
    "k0": 0.07471141,
    "dk": 0.00059199,
  },
  r"high-$\sqrt{s*}$": {
    "sigma0": 7250.0,
    "Ae" : 0.11251847,
    "Af" : 0.03217479,
    "ef" : 1.42594481,
    "k0" : 0.00033356,
    "dk" : 0.00031470,
  },
  "LEP/SLC": {
    "Ae" : 0.1515,
    "Af" : 0.1515,
    "ef" : 0.0
  }
}

#-------------------------------------------------------------------------------

def Af_fromAFB(AFB, Ae, ef):
  """ Calculate Af from AFB for given Ae and epsilon_f.
  """
  return (8./3. * AFB - ef) / (2 * Ae)
  
#-------------------------------------------------------------------------------

def AFB_at_mass(mass_label):
  """ Calculate the AFB value for the given mass label.
  """
  Ae = truth_vals[mass_label]["Ae"]
  Af = truth_vals[mass_label]["Af"]
  ef = truth_vals[mass_label]["ef"]
  return 3./8. * (ef + 2 * Ae * Af)

#-------------------------------------------------------------------------------

def Ae_from_taupol_LEPextrap(N_tautau, mass_label="LEP/SLC"):
  """ Extrapolate the Ae uncertainty from the tau polarisation measurement at 
      LEP to a measurement with a different number of tau pair production 
      events.
      The relative uncertainty is extrapolated, and scaled to the relevant 
      parameter values.
  """
  unc_Ae_LEP = 5.e-3
  N_Ztatau_LEP = 1724e3 / 3 # 1724e3 events on all charged lepton species
  par_scaling = truth_vals[mass_label]["Ae"]/truth_vals["LEP/SLC"]["Ae"]
  return unc_Ae_LEP / np.sqrt( N_tautau / N_Ztatau_LEP ) * par_scaling
      
#-------------------------------------------------------------------------------

def cov_to_relative(cov, mass_label):
  """ Transform the absolute AeAf covariance matrix to the relative covariance 
      matrix.
  """
  Ae_true = truth_vals[mass_label]["Ae"]
  Af_true = truth_vals[mass_label]["Af"]
  scaling = np.array([ [Ae_true**2, Ae_true*Af_true],
                       [Ae_true*Af_true, Af_true**2] ])
  return cov / scaling

#-------------------------------------------------------------------------------

def add_indep_Ae_to_cov(cov, unc_Ae):
  """ Add the an independent Ae measurement to the given covariance matrix.
  """
  inv_taupol_cov = np.array([[1/unc_Ae**2, 0], [0, 0]])
  return np.linalg.inv(np.linalg.inv(cov) + inv_taupol_cov)

#-------------------------------------------------------------------------------

def adjust_ebar(ebar, ls):
  """ Adjust the given errorbar linestyle.
  """
  ebar[-1][0].set_linestyle(ls)
  return ebar
  
def draw_ellipse(ax, rs, Ae_name, Af_name, mass_label, mumu_only=True, 
                 use_taupol=False, **kwargs):
  """ Draw the Ae, Af covariance matrix ellipse for a given result summary.
      By default use the Ae measurement from the (mumu only) fit, if requested
      use the Ae uncertainty one would get using all visible difermion final 
      states.
      Relative impact of beam polarisation not changed.
      => Only makes sense if both beams are polarised!
         (With single beam polarisation, even mumu produces result that is 
          dominated by polarisation uncertainty.)
  """
  i_Ae = rs.par_index(Ae_name)
  i_Af = rs.par_index(Af_name)
  full_cov = rs.cov_mat_avg
  AeAf_cov = np.array([[full_cov[i_Ae,i_Ae],full_cov[i_Af,i_Ae]],
                       [full_cov[i_Ae,i_Af],full_cov[i_Af,i_Af]]])
                       
  if not mumu_only:
    # Add the ALR measurement from other 2f final states 
    stat_scale = np.sqrt(3.36/(80.0-3.36)) # 3.36% mumu VS 80% visible Z decays
    unc_ALR_other = stat_scale * np.sqrt(AeAf_cov[0][0])
    AeAf_cov = add_indep_Ae_to_cov(AeAf_cov, unc_ALR_other)
    
  if use_taupol and (mass_label=="return-to-Z"):
    # Add the Ae measurement from tau polarisation
    lumi = rs.par_avg[rs.par_index("Lumi")] # Get the lumi of the setup
    N_tautau = lumi * truth_vals[mass_label]["sigma0"]
    # TODO HERE: Correct for different Ae val
    unc_Ae_taupol = Ae_from_taupol_LEPextrap(N_tautau, mass_label)
    
    AeAf_cov = add_indep_Ae_to_cov(AeAf_cov, unc_Ae_taupol)
                       
  AeAf_cov = cov_to_relative(AeAf_cov, mass_label)
  PS.confidence_ellipse(AeAf_cov, 1, 1, ax, n_std=1.0, **kwargs)

def draw_unpol_range(ax, unc_AFB, mass_label, **kwargs):
  """ Draw the range that the unpolarised collider can constrain in the Ae/Af
      plane, assuming epsilon_f to be known perfectly. 
  """
  val_AFB = AFB_at_mass(mass_label)
  AFB_low = val_AFB - unc_AFB 
  AFB_up = val_AFB + unc_AFB 

  Ae_true = truth_vals[mass_label]["Ae"]

  Ae_min, Ae_max = np.array(ax.get_xlim()) * Ae_true
  Ae_vals = np.linspace(Ae_min, Ae_max, 500)
  
  ef = truth_vals[mass_label]["ef"]
  Af_low = Af_fromAFB(AFB_low, Ae_vals, ef)
  Af_up = Af_fromAFB(AFB_up, Ae_vals, ef)
  
  # Scale to relative
  Af_true = truth_vals[mass_label]["Af"]
  x = Ae_vals/Ae_true
  y_low = Af_low/Af_true
  y_up = Af_up/Af_true
  
  # Draw the two bands
  p_low = ax.plot(x, y_low, **kwargs)
  kwargs['color'] = p_low[0].get_color()
  del kwargs['label']
  p_up = ax.plot(x, y_up, **kwargs)

def draw_unpol_ellipse(ax, unc_AFB, unc_Ae, mass_label, scale=1.0, **kwargs):
  """ Draw the Ae/Af ellipse for an unpolarised scenario that measures AFBmu in 
      muon pair production and Ae through tau polarisation.
  """
  Ae = truth_vals[mass_label]["Ae"]
  Af = truth_vals[mass_label]["Af"]
  ef = truth_vals[mass_label]["ef"]
  AFB = 3./8. * (ef + 2 * Ae * Af)
  
  # Transform the covariance matrix from AFB:Ae to Amu:Ae
  cov_AeAFB = np.array([[unc_Ae**2, 0.],
                        [0.,        unc_AFB**2]])
  transf_mat = np.array([
    [1.,                                            0.               ],
    [- 1./(2.*Ae**2) * (8./3. * AFB - ef),          8/3 * 1./(2.*Ae) ] ])
  cov_AeAf = np.matmul(np.matmul(transf_mat, cov_AeAFB), transf_mat.T) 
  cov_AeAf = cov_AeAf * scale**2
  
  # print(np.sqrt(cov_AeAf))
  # print(cov_AeAf[0][1] / np.sqrt(cov_AeAf[0][0]) / np.sqrt(cov_AeAf[1][1]))
  
  AeAf_cov = cov_to_relative(cov_AeAf, mass_label)
  PS.confidence_ellipse(AeAf_cov, 1, 1, ax, n_std=1.0, **kwargs)

def draw_FCCee_TeraZ(ax, scale=1.0, use_taupol=True, **kwargs):
  """ Draw the expected result for the FCCee Tera-Z.
      Either show only band from AFBmu measurement or show ellipse that also
      uses Ae from tau polarisation measurement.
  
      FCC-ee ref: https://link.springer.com/article/10.1140/epjst/e2019-900045-4
      LEP # Z-pol tautau events & Ae precision from tau polarisation:
        https://arxiv.org/abs/hep-ex/0312023
      
      Assumes an AFB measurement in the mumu channel of
        3e-6 (stat) (+) 9e-6 (syst from COM energy measurement)
      and an independent measurement of Ae from tau polarisation.
      For the Ae uncertainty I take the LEP uncertainty on Ae from tau
      polarisation (~0.005) and devide it by the increased statistics (10^7 more
      Z events at FCC-ee Tera-Z).
  """
  unc_AFB = np.sqrt((3e-6)**2 + (9e-6)**2)
  
  if use_taupol:
    N_Ztatau_FCCee = 1.5e11 # 1.7e11 tautau events
    # From: https://indico.fnal.gov/event/51940/contributions/232053/attachments/151016/194982/Alcaraz_EW-FCCee_EF04_20Jan2022.pdf
    # => dAe ~ 2.1e-5
    # LEP extrapolation gives: 9.192921402990923e-06
    # ~> LEP extrapolation seems fair, only slightly optimistic
    unc_Ae = Ae_from_taupol_LEPextrap(N_Ztatau_FCCee)
    
    draw_unpol_ellipse(ax, unc_AFB, unc_Ae, "LEP/SLC", scale, **kwargs)
  else:
    draw_unpol_range(ax, unc_AFB*scale, "LEP/SLC", **kwargs)

def draw_ILC_GigaZ(ax, scale=1.0, mumu_only=False, **kwargs):
  """ Draw the expected result for the ILC Giga-Z.
      Ae by default uses all difermion final states, or only from muon pair 
      production.
      If only muon pair production is used for Ae, then systematic uncertainty 
      is assumed negligible.
      Ref: https://arxiv.org/pdf/1908.11299.pdf
      Ref (hadronic w/o syst.): https://arxiv.org/pdf/1905.00220.pdf
      Assumes that the A_e and A_mu measurements are uncorrelated (which is 
      likely).
  """
  # Determine the Ae uncertainty
  # If all 2f used, assume Ae to be limited by polarisation uncertainty 
  # (5e-4 relative), else assume statistically limited (scaled from 3e-5 
  # absolute of hadrons)
  Ae_true = truth_vals["LEP/SLC"]["Ae"]
  unc_Ae = np.sqrt(69.91/3.366) * 3e-5 if mumu_only else 5e-4 * Ae_true
  
  # Assume that Amu will be limited by polarisation uncertainty
  # (this is a bit questionable, I'll stick with it here, statistics probably 
  # worse)
  Amu_true = truth_vals["LEP/SLC"]["Af"]
  unc_Amu = 5e-4 * Amu_true
  
  # Transform the covariance matrix from Ae:AFB to Ae:Amu
  cov_AeAf = np.array([[unc_Ae**2, 0.],
                       [0.,        unc_Amu**2]])
  
  # Also include the contribution of a GigaZ tau polarisation measurement
  # -> Contributes only an additional Ae measurement with rel. 2e-3 unc.
  if not mumu_only:                 
    N_tautau = 1.6e8
    unc_Ae_taupol = Ae_from_taupol_LEPextrap(N_tautau)
    cov_AeAf = add_indep_Ae_to_cov(cov_AeAf, unc_Ae_taupol)
                  
  # Transform to the covariance matrix on the relative Ae/Ae_true : Amu/Amu_true
  cov_AeAf = cov_AeAf * scale**2
  
  # print(np.sqrt(cov_AeAf))
  # print(cov_AeAf[0][1] / np.sqrt(cov_AeAf[0][0]) / np.sqrt(cov_AeAf[1][1]))
  
  AeAf_cov = cov_to_relative(cov_AeAf, "LEP/SLC")
  PS.confidence_ellipse(AeAf_cov, 1, 1, ax, n_std=1.0, **kwargs)

def draw_unpol_fit_range(ax, rs, AFB_name, mass_label, **kwargs):
  """ Draw the range that the unpolarised collider can constrain in the Ae/Af
      plane, assuming epsilon_f to be known perfectly. 
  """
  i_AFB = rs.par_index(AFB_name)
  unc_AFB = rs.unc_vec_avg[i_AFB]
  draw_unpol_range(ax, unc_AFB, mass_label, **kwargs)
  
def draw_unpol_real(ax, rs, AFB_name, mass_label, **kwargs):
  """ Draw estimate of realistic Ae/Af ellipse for unpolarised fit scenario.
      Assumes the AFB uncertainty from the given fit result, and assumes an Ae 
      measurement from tau polarisation.
      The Ae uncertainty is extrapolated from the LEP Ae uncertainty, using 
      simple luminosity scaling.
  """
  i_AFB = rs.par_index(AFB_name)
  unc_AFB = rs.unc_vec_avg[i_AFB]
  
  i_Lumi = rs.par_index("Lumi")
  lumi = rs.par_avg[i_Lumi]
  N_tautau_unpol = lumi * truth_vals[mass_label]["sigma0"]
  
  # TODO HERE: Correct for different Ae val
  unc_Ae = Ae_from_taupol_LEPextrap(N_tautau_unpol, mass_label)
  
  draw_unpol_ellipse(ax, unc_AFB, unc_Ae, mass_label, **kwargs)
  
def draw_unpol_opt(ax, rs, AFB_name, mass_label, **kwargs):
  """ Draw optimistic errorbars for the unpolarised scenarios assuming Ae or Af 
      perfectly known / fixed.
  """
  i_AFB = rs.par_index(AFB_name)
  unc_AFB = rs.unc_vec_avg[i_AFB]
  
  Ae_true = truth_vals[mass_label]["Ae"]
  Af_true = truth_vals[mass_label]["Af"]
  ef_true = truth_vals[mass_label]["ef"]
  
  unc_AFB = rs.unc_vec_avg[i_AFB]
  val_AFB = AFB_at_mass(mass_label)
  AFB_low = val_AFB - unc_AFB 
  AFB_up = val_AFB + unc_AFB 

  Af_low = Af_fromAFB(AFB_low, Ae_true, ef_true)
  Af_up = Af_fromAFB(AFB_up, Ae_true, ef_true)
  
  unc_Af_low = Af_true - Af_low
  unc_Af_up = Af_up - Af_true
  yerr = np.array([[unc_Af_low],[unc_Af_up]])
  
  labels=[None, None]
  if 'label' in kwargs:
    base_label = kwargs['label']
    labels = [
      "{}, \n{{$A_{{\mu}},\epsilon_{{\mu}}$, $P$}} fixed".format(base_label),
      "{}, \n{{$A_e,\epsilon_{{\mu}}$, $P$}} fixed".format(base_label) ]
  del kwargs['label']
  
  # Scale to relative
  yerr = yerr/Af_true
  
  adjust_ebar(ax.errorbar([1],[1],yerr=yerr,label=labels[1],**kwargs),ls=':')


def set_ylim(ax, rs_1pol, rs_0pol_2, Ae_name, Af_name, AFB_name, mass_label):
  """ Set some sensible limits using uncertainties from collider results with 
      only electron polarisation and without polarisation.
  """
  Ae = truth_vals[mass_label]["Ae"]
  Af = truth_vals[mass_label]["Af"]
  ef = truth_vals[mass_label]["ef"]
  
  unc_AFB = rs_0pol_2.unc_vec_avg[rs_0pol_2.par_index(AFB_name)]
  val_AFB = AFB_at_mass(mass_label)
  AFB_low = val_AFB - unc_AFB 
  AFB_up = val_AFB + unc_AFB 
  Af_low = Af_fromAFB(AFB_low, Ae, ef)
  Af_up = Af_fromAFB(AFB_up, Ae, ef)
  
  unc_Af_low = Af - Af_low
  unc_Af_up = Af_up - Af
  unc_Ae = rs_1pol.unc_vec_avg[rs_1pol.par_index(Ae_name)]
  
  # Transform to relative numbers
  x_unc = unc_Ae/Ae
  y_low, y_up = unc_Af_low/Af, unc_Af_up/Af
  
  ax.set_xlim([1 - 1.2 * x_unc, 1 + 1.2 * x_unc])
  ax.set_ylim([1 - 1.2 * y_low, 1 + 1.2 * y_up])

def draw_setups_withZpoleRuns(mrr, ax, Ae_name, Af_name, AFB_name, mass_label, 
                              mumu_only=True):
  """ Draw all the different visualisations for the Ae-Af uncertainties from the 
      different collider setups, including Z-pole future collider studies.
  """ 
  if mass_label != "return-to-Z":
    raise Exception("Z pole runs can only be drawn for return-to-Z.")
  
  # Recover all result summaries 
  rs_2polExt = mrr.get(2000, "2polExt_LPcnstr", "MuAccFree", "mumu_free").result_summary()
  rs_2pol = mrr.get(2000, "2pol_LPcnstr", "MuAccFree", "mumu_free").result_summary()
  rs_1pol = mrr.get(2000, "1pol_LPcnstr", "MuAccFree", "mumu_free").result_summary()
  rs_0pol_2 = mrr.get(2000, "0pol_LPcnstr", "MuAccFree", "mumu_unpol").result_summary()
  rs_0pol_10 = mrr.get(10000, "0pol_LPcnstr", "MuAccFree", "mumu_unpol").result_summary()

  # Get the colors of the color cycle (to get manual control over them)
  colors =  plt.rcParams['axes.prop_cycle'].by_key()['color']
  
  # Set some sensible axis limits
  set_ylim(ax, rs_1pol, rs_0pol_2, Ae_name, Af_name, AFB_name, mass_label)
  
  # Draw ellipse for setup with only electron polarisation
  # => No point to add non-mumu final states, since Ae is systematically limited
  draw_ellipse(ax, rs_1pol, Ae_name, Af_name, mass_label, mumu_only=True, use_taupol=not mumu_only ,ls="-", lw=5.0, edgecolor=colors[2], facecolor='none', label="(80,0), 2ab$^{-1}$", zorder=2)
  
  # Draw the fully polarised setups as ellipses
  # => If requested, add Ae measurement from non-mumu final states
  draw_ellipse(ax, rs_2pol, Ae_name, Af_name, mass_label, mumu_only=mumu_only, use_taupol=not mumu_only, ls="-", lw=5.0, edgecolor=colors[1], facecolor='none', label="(80,30), 2ab$^{-1}$", zorder=2)
  draw_ellipse(ax, rs_2polExt, Ae_name, Af_name, mass_label, mumu_only=mumu_only, use_taupol=not mumu_only, ls="-", lw=3.5, alpha=0.9, edgecolor=colors[0], facecolor='none', label="(80/0,30/0), 2ab$^{-1}$", zorder=2)

  # Draw limits for the unpolarised setups
  label_2 = "(0,0), 2ab$^{-1}$, \n{$\epsilon_{\mu}$, $P$} fixed"
  label_10 = "(0,0), 10ab$^{-1}$, \n{$\epsilon_{\mu}$, $P$} fixed"
  if mumu_only:
    draw_unpol_fit_range(ax, rs_0pol_2, AFB_name, mass_label, lw=5.0, color=colors[3], zorder=1, label=label_2)
    draw_unpol_fit_range(ax, rs_0pol_10, AFB_name, mass_label, lw=5.0, color=colors[4], zorder=1, label=label_10)
  else:
    draw_unpol_real(ax, rs_0pol_2, AFB_name, mass_label, label=label_2, ls="-", lw=5.0, edgecolor=colors[3], facecolor='none', zorder=2)
    draw_unpol_real(ax, rs_0pol_10, AFB_name, mass_label, label=label_10, ls="-", lw=5.0, edgecolor=colors[4], facecolor='none', zorder=2)
  
  scale_FCCee = 5.
  arxiv_FCCee = "1601.03849"
  FCCee_label="FCCee (Tera-Z)\nScaled $\\bf{{x{}}}$\narXiv:{}".format(int(scale_FCCee),arxiv_FCCee)
  FCCee_kwargs_mumu_only = { "label":FCCee_label, "zorder":3, "ls":"--", "lw":5.0, "color":colors[5]}
  FCCee_kwargs_with_taup = { "label":FCCee_label, "zorder":3, "ls":"--", "lw":5.0, "edgecolor":colors[5], "facecolor":'none'}
  FCCee_kwargs = FCCee_kwargs_mumu_only if mumu_only else FCCee_kwargs_with_taup
  draw_FCCee_TeraZ(ax, scale=scale_FCCee, use_taupol=not mumu_only, **FCCee_kwargs)
  scale_ILC = 5.
  arxiv_ILC = "1908.11299"
  draw_ILC_GigaZ(ax, scale=scale_ILC, mumu_only=mumu_only, label="ILC (Giga-Z)\nScaled $\\bf{{x{}}}$\narXiv:{}".format(int(scale_ILC),arxiv_ILC), zorder=3, ls="--", lw=5.0, edgecolor=colors[6], facecolor='none')
    
  # Reset some sensible axis limits
  set_ylim(ax, rs_1pol, rs_0pol_2, Ae_name, Af_name, AFB_name, mass_label)

def draw_setups(mrr, ax, Ae_name, Af_name, AFB_name, mass_label):
  """ Draw all the different visualisations for the Ae-Af uncertainties from the 
      different collider setups.
  """ 
  # Recover all result summaries 
  rs_2polExt = mrr.get(2000, "2polExt_LPcnstr", "MuAccFree", "mumu_free").result_summary()
  rs_2pol = mrr.get(2000, "2pol_LPcnstr", "MuAccFree", "mumu_free").result_summary()
  rs_1pol = mrr.get(2000, "1pol_LPcnstr", "MuAccFree", "mumu_free").result_summary()
  rs_0pol_2 = mrr.get(2000, "0pol_LPcnstr", "MuAccFree", "mumu_unpol").result_summary()
  rs_0pol_10 = mrr.get(10000, "0pol_LPcnstr", "MuAccFree", "mumu_unpol").result_summary()

  # Get the colors of the color cycle (to get manual control over them)
  colors =  plt.rcParams['axes.prop_cycle'].by_key()['color']
  
  # Set some sensible axis limits
  set_ylim(ax, rs_1pol, rs_0pol_2, Ae_name, Af_name, AFB_name, mass_label)
  
  # Draw the polarised setups as ellipses
  draw_ellipse(ax, rs_1pol, Ae_name, Af_name, mass_label, ls="-", lw=5.0, edgecolor=colors[2], facecolor='none', label="(80,0), 2ab$^{-1}$", zorder=2)
  draw_ellipse(ax, rs_2pol, Ae_name, Af_name, mass_label, ls="-", lw=5.0, edgecolor=colors[1], facecolor='none', label="(80,30), 2ab$^{-1}$", zorder=2)
  draw_ellipse(ax, rs_2polExt, Ae_name, Af_name, mass_label, ls="-", lw=3.5, alpha=0.9, edgecolor=colors[0], facecolor='none', label="(80/0,30/0), 2ab$^{-1}$", zorder=2)

  # Draw optimistic and less optimistic limits for the unpolarised setups
  draw_unpol_opt(ax, rs_0pol_2, AFB_name, mass_label, color=colors[3], lw=5, capsize=15, capthick=5, alpha=0.9, label="(0,0), 2ab$^{-1}$", ls='none')
  draw_unpol_opt(ax, rs_0pol_10, AFB_name, mass_label, color=colors[4], lw=5, capsize=15, capthick=5, alpha=0.9, label="(0,0), 10ab$^{-1}$", ls='none')
  
  draw_unpol_fit_range(ax, rs_0pol_2, AFB_name, mass_label, lw=5.0, color=colors[3], label="(0,0), 2ab$^{-1}$, \n{$\epsilon_{\mu}$, $P$} fixed", zorder=1)
  draw_unpol_fit_range(ax, rs_0pol_10, AFB_name, mass_label, lw=5.0, color=colors[4], label="(0,0), 10ab$^{-1}$, \n{$\epsilon_{\mu}$, $P$} fixed", zorder=1)
  
  # Reset some sensible axis limits
  set_ylim(ax, rs_1pol, rs_0pol_2, Ae_name, Af_name, AFB_name, mass_label)
  
def draw_true_point(ax, mass_label, **kwargs):
  """ Mark the true Ae-Af point on the plot.
  """
  if mass_label in truth_vals:
    ax.plot([1],[1], 
            **kwargs)
  else:
    raise Exception("Unknown label {}".format(mass_label))

#-------------------------------------------------------------------------------

def reorder_legend_handles(ax, draw_colliders=False, mumu_only=True):
  """ Reorder the legend handles to make the legend look more orderly.
  """
  handles, _ = ax.get_legend_handles_labels()
  if (len(handles) == 8) and draw_colliders and mumu_only:
    reordering = [4,5,6,0,1,3,7,2]
  elif (len(handles) == 8) and draw_colliders and not mumu_only:
    reordering = [1,2,3,4,5,0,7,6]
  elif (len(handles) == 8) and not draw_colliders:
    reordering = [3,4,5,0,1,6,7,2]
  else:
    raise Exception("Not prepared for {} labels.".format(len(handles)))
    
  return [handles[i] for i in reordering]

#-------------------------------------------------------------------------------

def legend_title(label, draw_colliders=False, mumu_only=True):
  """ Get an appropriate legend title for the scenario.
  """
  process_str = "$e^+e^-\\rightarrow\\mu^+\\mu^-$"
  if draw_colliders and not mumu_only:
    process_str = "$e^+e^-\\rightarrow f\\bar{f}$"
    
  mass_str = label
  if draw_colliders:
    mass_str = "{} / Z-pole".format(label)
  
  return process_str + " (" + mass_str + ")"

#-------------------------------------------------------------------------------

def AeAf_comparison_plot(mrr, output_dir, mass_range, label, draw_colliders=False, mumu_only=True):
  """ Create the Ae - Af plane comparison plot for the different collider 
      setups.
  """
  # Figure basics
  fig = plt.figure(figsize=(12.5,7.5), tight_layout=True) # 
  ax = plt.gca()
  ax.set_xlabel("$A_e^{meas}/A_e^{true}$", fontsize=28)
  ax.set_ylabel("$A_{\mu}^{meas}/A_{\mu}^{true}$", fontsize=28)

  # Get the parameter names
  par_base_names = np.array([
   "s0_2f_mu", "Ae_2f_mu", "Af_2f_mu", "ef_2f_mu", "AFB_2f_mu", "k0_2f_mu", "dk_2f_mu"])
  par_names = np.array(["{}_{}".format(par,mass_range) for par in par_base_names])
  s0_name, Ae_name, Af_name, ef_name, AFB_name, k0_name, dk_name = par_names 

  # Draw all the necessary lines
  if draw_colliders:
    draw_setups_withZpoleRuns(mrr, ax, Ae_name, Af_name, AFB_name, label, mumu_only)
  else:
    draw_setups(mrr, ax, Ae_name, Af_name, AFB_name, label)
  draw_true_point(ax, label, marker="X", ls="none", ms=15, color="black", label="Truth")

  # Create a useful legend
  handles = reorder_legend_handles(ax, draw_colliders, mumu_only)
  legend = plt.legend(handles=handles, title="$(P_{{e^-}}[\\%],P_{{e^+}}[\\%])$, $L$", ncol=1, fontsize=20, title_fontsize=24, bbox_to_anchor=(1.02, .0), loc='lower left')
  ax.set_title(legend_title(label, draw_colliders, mumu_only))

  # Reduce the number of axis ticks
  ax.locator_params(axis='x', nbins=4)
  ax.locator_params(axis='y', nbins=4)

  # Save the plot in files
  for out_format in ["pdf","png"]:
    format_dir = "{}/{}".format(output_dir,out_format)
    IOSH.create_dir(format_dir)
    collider_str = "_wColliders{}".format("" if mumu_only else "_withtaupol") if draw_colliders else ""
    fig.savefig("{}/2f_pars_{}{}.{}".format(format_dir,mass_range,collider_str,out_format), transparent=True, bbox_extra_artists=[legend], bbox_inches='tight')
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
    IODPS.DifParamSetup("mumu_unpol", "free", "fixed", "fixed", "free->AFB", "free->k0", "fixed")
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
  AeAf_comparison_plot(mrr, output_dir, "81to101", "return-to-Z", draw_colliders=True, mumu_only=True)
  AeAf_comparison_plot(mrr, output_dir, "81to101", "return-to-Z", draw_colliders=True, mumu_only=False)
  AeAf_comparison_plot(mrr, output_dir, "180to275", r"high-$\sqrt{s*}$")
  
if __name__ == "__main__":
  main()