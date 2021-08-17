""" Code for translating the parameter names into their corresponding symbols.
"""

import numpy as np

default_symbol_dict = {
  'Lumi' : r"$L$",
  'ePol-' : r"$P_{e^-}^{-}$",
  'ePol+' : r"$P_{e^-}^{+}$",
  'pPol-' : r"$P_{e^+}^{-}$",
  'pPol+' : r"$P_{e^+}^{+}$",
  'ePol0' : r"$P_{e^-}^{0}$",
  'pPol0' : r"$P_{e^+}^{0}$",
  'Delta-g1Z' : r"$g_{1}^{Z}$",
  'Delta-kappa_gamma' : r"$\kappa_{\gamma}$",
  'Delta-lambda_gamma' : r"$\lambda_{\gamma}$",
  'DeltaA_WW_muminus' : r"$A_{LR} (W^{-})$",
  'DeltaA_WW_muplus' : r"$A_{LR} (W^{+})$",
  'Ae_2f_mu_81to101' : r"$A_e (m_{Z})$",
  'Af_2f_mu_81to101' : r"$A_{\mu} (m_{Z})$",
  'ef_2f_mu_81to101' : r"$\epsilon_{\mu} (m_{Z})$",
  'k0_2f_mu_81to101' : r"$k_0 (m_{Z})$",
  'dk_2f_mu_81to101' : r"$\Delta k (m_{Z})$",
  'Ae_2f_mu_180to275' : r"$A_e (250GeV)$",
  'Af_2f_mu_180to275' : r"$A_{\mu} (250GeV)$",
  'ef_2f_mu_180to275' : r"$\epsilon_{\mu} (250GeV)$",
  'k0_2f_mu_180to275' : r"$k_0 (250GeV)$",
  'dk_2f_mu_180to275' : r"$\Delta k (250GeV)$",
  'AFB_2f_mu_81to101' : r"$A_{FB,0}^{\mu} (m_{Z})$",
  'AFB_2f_mu_180to275' : r"$A_{FB,0}^{\mu} (250GeV)$",
  's0_2f_mu_81to101' : r"$\sigma_0/\sigma_0^{SM} (m_{Z})$",
  's0_2f_mu_180to275' : r"$\sigma_0/\sigma_0^{SM} (250GeV)$",
  'ScaleTotChiXS_WW_muminus' : "$\sigma_0/\sigma_0^{SM}(W^{-})$",
  'ScaleTotChiXS_WW_muplus' : "$\sigma_0/\sigma_0^{SM}(W^{+})$",
  'MuonAcc_dCenter' : r"$\Delta c$",
  'MuonAcc_dWidth' : r"$\Delta w$"
}

def names_to_symbols(par_names, symbol_dict=default_symbol_dict):
  """ Transform the array of parameter names to the corresponding array of 
      symbols as given by the symbol dictionary.
  """
  return np.asarray(list(symbol_dict.values()))[
          np.nonzero( list(symbol_dict.keys()) == par_names[:,None] )[1] ]