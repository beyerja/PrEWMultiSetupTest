#ifndef LIB_PREWRUNEXAMPLE_RUNINFOS_H
#define LIB_PREWRUNEXAMPLE_RUNINFOS_H 1

// Includes from PrEWUtils
#include "SetupHelp/SetupInfos.h"

using namespace PrEWUtils::SetupHelp;

namespace RunInfos {
  
const double rel_L_constr = 3.0e-3;
const double rel_P_constr = 2.5e-3;
const double abs_P_constr = 2.5e-3;

// -----------------------------------------------------------------------------

inline RunInfo setup_2pol_LPcnstr(int energy, double lumi) {
  PrEWUtils::SetupHelp::RunInfo run(energy);
  run.set_lumi(lumi);
  run.add_pol("ePol-", 0.8);
  run.add_pol("ePol+", 0.8);
  run.add_pol("pPol-", 0.3);
  run.add_pol("pPol+", 0.3);
  run.add_lumi_constr(lumi, lumi * rel_L_constr);
  run.add_pol_constr("ePol-", 0.8, 0.8 * rel_P_constr);
  run.add_pol_constr("ePol+", 0.8, 0.8 * rel_P_constr);
  run.add_pol_constr("pPol-", 0.3, 0.3 * rel_P_constr);
  run.add_pol_constr("pPol+", 0.3, 0.3 * rel_P_constr);
  run.add_pol_config("e-p+", "ePol-", "pPol+", "-", "+", 0.45);
  run.add_pol_config("e+p-", "ePol+", "pPol-", "+", "-", 0.45);
  run.add_pol_config("e-p-", "ePol-", "pPol-", "-", "-", 0.05);
  run.add_pol_config("e+p+", "ePol+", "pPol+", "+", "+", 0.05);
  return run;
}

inline RunInfo setup_2pol_LPfixed(int energy, double lumi) {
  auto run = setup_2pol_LPcnstr(energy, lumi);
  run.fix_lumi();
  run.fix_pol("ePol-");
  run.fix_pol("ePol+");
  run.fix_pol("pPol-");
  run.fix_pol("pPol+");
  return run;
}

inline RunInfo setup_2pol_Lconstr_Pfixed(int energy, double lumi) {
  auto run = setup_2pol_LPcnstr(energy, lumi);
  run.fix_pol("ePol-");
  run.fix_pol("ePol+");
  run.fix_pol("pPol-");
  run.fix_pol("pPol+");
  return run;
}

// -----------------------------------------------------------------------------

inline RunInfo setup_1pol_LPcnstr(int energy, double lumi) {
  PrEWUtils::SetupHelp::RunInfo run(energy);
  run.set_lumi(lumi);
  run.add_pol("ePol-", 0.8);
  run.add_pol("ePol+", 0.8);
  run.add_pol("pPol0", 0.0);
  run.add_lumi_constr(lumi, lumi * rel_L_constr);
  run.add_pol_constr("ePol-", 0.8, 0.8 * rel_P_constr);
  run.add_pol_constr("ePol+", 0.8, 0.8 * rel_P_constr);
  run.add_pol_constr("pPol0", 0.0, abs_P_constr);
  run.add_pol_config("e-p0", "ePol-", "pPol0", "-", "+", 0.5);
  run.add_pol_config("e+p0", "ePol+", "pPol0", "+", "+", 0.5);
  return run;
}

inline RunInfo setup_1pol_LPfixed(int energy, double lumi) {
  auto run = setup_1pol_LPcnstr(energy, lumi);
  run.fix_lumi();
  run.fix_pol("ePol-");
  run.fix_pol("ePol+");
  run.fix_pol("pPol0");
  return run;
}

inline RunInfo setup_1pol_Lconstr_Pfixed(int energy, double lumi) {
  auto run = setup_1pol_LPcnstr(energy, lumi);
  run.fix_pol("ePol-");
  run.fix_pol("ePol+");
  run.fix_pol("pPol0");
  return run;
}


inline RunInfo setup_1pol_LPcnstr_P0fixed(int energy, double lumi) {
  auto run = setup_1pol_LPcnstr(energy, lumi);
  run.fix_pol("pPol0");
  return run;
}

// -----------------------------------------------------------------------------

inline RunInfo setup_0pol_LPcnstr(int energy, double lumi) {
  RunInfo run(energy);
  run.set_lumi(lumi);
  run.add_pol("ePol0", 0.0);
  run.add_pol("pPol0", 0.0);
  run.add_lumi_constr(lumi, lumi * rel_L_constr);
  run.add_pol_constr("ePol0", 0.0, abs_P_constr);
  run.add_pol_constr("pPol0", 0.0, abs_P_constr);
  run.add_pol_config("e0p0", "ePol0", "pPol0", "+", "+", 1.0);
  return run;
}

inline RunInfo setup_0pol_LPfixed(int energy, double lumi) {
  auto run = setup_0pol_LPcnstr(energy, lumi);
  run.fix_lumi();
  run.fix_pol("ePol0");
  run.fix_pol("pPol0");
  return run;
}

inline RunInfo setup_0pol_Lconstr_P0fixed(int energy, double lumi) {
  auto run = setup_0pol_LPcnstr(energy, lumi);
  run.fix_pol("ePol0");
  run.fix_pol("pPol0");
  return run;
}

// -----------------------------------------------------------------------------

} // namespace RunInfos

#endif