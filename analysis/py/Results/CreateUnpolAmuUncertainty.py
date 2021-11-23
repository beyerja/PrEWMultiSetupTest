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

def calc_AFB(Ae, Af, ef):
  """ Calculate AFB from Ae, Af, and epsilon_f.
  """
  return 3./8. * (ef + 2 * Ae * Af)

#-------------------------------------------------------------------------------

def Af_unc(Af, AFB, Ae, d_AFB, d_Pol0, d_Ae=0):
  """ Estimate the uncertainty on Af.
      Needs Af, AFB, and Ae and the uncertainties:
        d_AFB: AFB uncertainty from fit
        d_Pol0: Uncertainty on each of the individual 0-polarisations
        d_Ae: uncertainty on Ae
  """
  return np.abs(Af) * np.sqrt(
            (d_AFB/AFB)**2 + ((1-Ae**2)/Ae)**2 * 2 * d_Pol0**2 + (d_Ae/Ae)**2 )
  
#-------------------------------------------------------------------------------

def draw_Af_unc_range(ax, rs, AFB_name, dPol_range, **kwargs):
  """ Draw the Af uncertainty for a range of polarisation uncertainties.
  """
  Ae = truth_vals["return-to-Z"]["Ae"]
  Af = truth_vals["return-to-Z"]["Af"]
  ef = truth_vals["return-to-Z"]["ef"]
  AFB = calc_AFB(Ae, Af, ef)

  i_AFB = rs.par_index(AFB_name)
  unc_AFB = rs.unc_vec_avg[i_AFB]

  unc_Af = Af_unc(Af, AFB, Ae, unc_AFB, dPol_range) * 1e3
  
  ax.plot(dPol_range, unc_Af, **kwargs)

def Af_uncertainty_plot(mrr, output_dir, mass_range, label):
  """ Draw the Af uncertainties for different unpolarised setups depending on 
      the polarisation uncertainty.
  """
  # Figure basics
  fig = plt.figure(figsize=(7.5,5.5), tight_layout=True)
  ax = plt.gca()
  ax.set_xlabel("$\Delta P$ or $\Delta A_e / \sqrt{2}$")
  ax.set_ylabel("$\Delta A_{\mu}\,[10^{-3}]$")
  
  rs_0pol_2 = mrr.get(2000, "0pol_LPcnstr", "MuAccFree", "mumu_unpol").result_summary()
  rs_0pol_10 = mrr.get(10000, "0pol_LPcnstr", "MuAccFree", "mumu_unpol").result_summary()

  dPol_range = np.logspace(-5, -2, num=200)
  
  AFB_name = "AFB_2f_mu_" + mass_range
  draw_Af_unc_range(ax, rs_0pol_2, AFB_name, dPol_range, label="$L=2\,$ab$^{-1}$")
  draw_Af_unc_range(ax, rs_0pol_10, AFB_name, dPol_range, label="$L=10\,$ab$^{-1}$")

  ax.set_xscale('log')
  ax.set_ylim(0, ax.get_ylim()[1])
  ax.set_xlim(np.amin(dPol_range), np.amax(dPol_range))

  legend = plt.legend(title="$e^+e^-\\rightarrow\mu^+\mu^-$ ({})\nunpolarised, $\Delta\epsilon_{{\mu}}=0$".format(label), fontsize=17, title_fontsize=17)

  # Save the plot in files
  for out_format in ["pdf","png"]:
    format_dir = "{}/{}".format(output_dir,out_format)
    IOSH.create_dir(format_dir)
    fig.savefig("{}/Af_unc_{}.{}".format(format_dir,mass_range,out_format), transparent=True)
  plt.close(fig)

#-------------------------------------------------------------------------------

def main():
  log.basicConfig(level=log.INFO)
  PDF.set_default_mpl_format()
  os.environ["USE_N_CORES"] = "7"
  
  output_base = "../../../output"
  fit_output_base = "{}/run_outputs".format(output_base)
  
  unpol_lumi_setups = [ 2000, 10000 ]
  unpol_run_setups = [
    IORS.RunSetup("0pol_LPcnstr",  0,  0, "constrained", "constrained")
  ]
  muacc_setups = [
    IOMAS.MuAccSetup("MuAccFree", 0.9925, "free", "free"),
  ]
  unpol_difparam_setups = [
    IODPS.DifParamSetup("mumu_unpol", "free", "fixed", "fixed", "free->AFB", "free->k0", "fixed")
  ]
  
  mrr = IOMRR.MultiResultReader(fit_output_base, unpol_lumi_setups, 
                                unpol_run_setups, muacc_setups, 
                                unpol_difparam_setups)

  # Output directories
  output_dir = "{}/plots/AfUncertainty".format(output_base)

  Af_uncertainty_plot(mrr, output_dir, "81to101", "return-to-Z")
  Af_uncertainty_plot(mrr, output_dir, "180to275", r"high-$\sqrt{s*}$")
  
if __name__ == "__main__":
  main()