# Local modules
import Setups.DifParamSetup as IODPS
import Setups.MuAccSetup as IOMAS
import Setups.RunSetup as IORS

default_lumi_setups = [
  1000,
  2000,
  10000
]

default_muacc_setups = [
  IOMAS.MuAccSetup("MuAccFree", 0.9925, "free", "free"),
  IOMAS.MuAccSetup("MuAccFixd", 0.9925, "fixed", "fixed")
]

default_pol_run_setups = [
  IORS.RunSetup("2pol_LPcnstr", 80, 30, "constrained", "constrained"),
  IORS.RunSetup("2pol_LPfixed", 80, 30, "fixed", "fixed"),
  IORS.RunSetup("2pol_Lconstr_Pfixed", 80, 30, "constrained", "fixed"),
  IORS.RunSetup("2pol_Lfixed_Pconstr", 80, 30, "fixed", "constrained"),
  IORS.RunSetup("2polExt_Lconstr_Pfixed", 80, 30, "constrained", "fixed"),
  IORS.RunSetup("2polExt_Lconstr_Pfixed", 80, 30, "constrained", "fixed"),
  IORS.RunSetup("2polExt_Lconstr_Pfixed", 80, 30, "constrained", "fixed"),
  IORS.RunSetup("2polExt_Lfixed_Pconstr", 80, 30, "fixed", "constrained"),
  IORS.RunSetup("1pol_LPcnstr", 80,  0, "constrained", "constrained"),
  IORS.RunSetup("1pol_LPfixed", 80,  0, "fixed", "fixed"),
  IORS.RunSetup("1pol_Lconstr_Pfixed", 80,  0, "constrained", "fixed"),
  IORS.RunSetup("1pol_LPcnstr_P0fixed", 80,  0, "constrained", "constrained, P0 fixed"),
  IORS.RunSetup("1pol_Lfixed_Pconstr", 80, 0, "fixed", "constrained")
]

default_unpol_run_setups = [
  IORS.RunSetup("0pol_LPcnstr",  0,  0, "constrained", "constrained"),
  IORS.RunSetup("0pol_LPfixed",  0,  0, "fixed", "fixed"),
  IORS.RunSetup("0pol_Lconstr_P0fixed",  0,  0, "constrained", "fixed"),
  IORS.RunSetup("0pol_Lfixed_P0constr",  0,  0, "fixed", "constrained")
]

default_pol_difparam_setups = [                         # s0, Ae, Af, ef, kL, kR
  IODPS.DifParamSetup("mumu_free",                      "free", "free", "free", "free", "free", "free"),
  IODPS.DifParamSetup("mumu_fixed_ks",                  "free", "free", "free", "free", "fixed", "fixed"),
  IODPS.DifParamSetup("mumu_LEPconstr_Ae_Af",           "free", "constrained", "constrained", "constrained", "constrained", "constrained", constr_type="LEP"),
  IODPS.DifParamSetup("mumu_LEPconstr_Ae_Af_fixed_ks",  "free", "constrained", "constrained", "constrained", "fixed", "fixed", constr_type="LEP"),
]

default_unpol_difparam_setups = [
  IODPS.DifParamSetup("mumu_ILCconstr_Ae_Af_ef_ks",       "free", "constrained", "constrained", "constrained", "constrained", "constrained", constr_type="ILC"),
  IODPS.DifParamSetup("mumu_ILCconstr_Ae_Af_ef_fixed_ks", "free", "constrained", "constrained", "constrained", "fixed", "fixed", constr_type="ILC"),
  IODPS.DifParamSetup("mumu_AFB_k0_fixed_Ae_Af_kR",       "free", "fixed", "fixed", "free->AFB", "free->k0", "fixed")
]