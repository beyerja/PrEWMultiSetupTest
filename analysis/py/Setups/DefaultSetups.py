# Local modules
import Setups.DifParamSetup as IODPS
import Setups.MuAccSetup as IOMAS
import Setups.RunSetup as IORS

default_lumi_setups = [
  1000,
  2000,
  10000
]

default_run_setups = [
  IORS.RunSetup("2pol_LPcnstr", 80, 30, "constrained", "constrained"),
  IORS.RunSetup("1pol_LPcnstr", 80,  0, "constrained", "constrained"),
  IORS.RunSetup("0pol_LPcnstr",  0,  0, "constrained", "constrained"),
  IORS.RunSetup("2pol_LPfixed", 80, 30, "fixed", "fixed"),
  IORS.RunSetup("1pol_LPfixed", 80,  0, "fixed", "fixed"),
  IORS.RunSetup("0pol_LPfixed",  0,  0, "fixed", "fixed")
]

default_muacc_setups = [
  IOMAS.MuAccSetup("MuAccFree", 0.9925, "free", "free"),
  IOMAS.MuAccSetup("MuAccFixd", 0.9925, "fixed", "fixed")
]

default_difparam_setups = [
  IODPS.DifParamSetup("mumu_free",                        "free", "free", "free", "free", "free", "free"),
  IODPS.DifParamSetup("mumu_fixed_ks",                    "free", "free", "free", "free", "fixed", "fixed"),
  IODPS.DifParamSetup("mumu_LEPconstr_Ae_Af_ef_ks",       "free", "constrained", "constrained", "constrained", "constrained", "constrained", constr_type="LEP"),
  IODPS.DifParamSetup("mumu_LEPconstr_Ae_Af_ef_fixed_ks", "free", "constrained", "constrained", "constrained", "fixed", "fixed", constr_type="LEP"),
  IODPS.DifParamSetup("mumu_ILCconstr_Ae_Af_ef_ks",       "free", "constrained", "constrained", "constrained", "constrained", "constrained", constr_type="ILC"),
  IODPS.DifParamSetup("mumu_ILCconstr_Ae_Af_ef_fixed_ks", "free", "constrained", "constrained", "constrained", "fixed", "fixed", constr_type="ILC")
]