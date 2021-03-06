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

inline RunInfo setup_2pol_Lfixed_Pconstr(int energy, double lumi) {
  auto run = setup_2pol_LPcnstr(energy, lumi);
  run.fix_lumi();
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

inline RunInfo setup_2pol_LPfixed(int energy, double lumi) {
  auto run = setup_2pol_Lconstr_Pfixed(energy, lumi);
  run.fix_lumi();
  return run;
}

// -----------------------------------------------------------------------------
// Extended scenarios with 2 beam polarisation and also using 0-polarisation

inline RunInfo setup_2polExt_LPcnstr(int energy, double lumi) {
  PrEWUtils::SetupHelp::RunInfo run(energy);
  run.set_lumi(lumi);
  run.add_pol("ePol-", 0.8);
  run.add_pol("ePol+", 0.8);
  run.add_pol("pPol-", 0.3);
  run.add_pol("pPol+", 0.3);
  run.add_pol("ePol0", 0.0);
  run.add_pol("pPol0", 0.0);
  run.add_lumi_constr(lumi, lumi * rel_L_constr);
  run.add_pol_constr("ePol0", 0.0, abs_P_constr);
  run.add_pol_constr("pPol0", 0.0, abs_P_constr);
  run.add_pol_constr("ePol-", 0.8, 0.8 * rel_P_constr);
  run.add_pol_constr("ePol+", 0.8, 0.8 * rel_P_constr);
  run.add_pol_constr("pPol-", 0.3, 0.3 * rel_P_constr);
  run.add_pol_constr("pPol+", 0.3, 0.3 * rel_P_constr);
  run.add_pol_config("e-p+", "ePol-", "pPol+", "-", "+", 0.36);
  run.add_pol_config("e+p-", "ePol+", "pPol-", "+", "-", 0.36);
  run.add_pol_config("e-p-", "ePol-", "pPol-", "-", "-", 0.04);
  run.add_pol_config("e+p+", "ePol+", "pPol+", "+", "+", 0.04);
  run.add_pol_config("e0p-", "ePol0", "pPol-", "+", "-", 0.04);
  run.add_pol_config("e0p+", "ePol0", "pPol+", "+", "+", 0.04);
  run.add_pol_config("e-p0", "ePol-", "pPol0", "-", "+", 0.04);
  run.add_pol_config("e+p0", "ePol+", "pPol0", "+", "+", 0.04);
  run.add_pol_config("e0p0", "ePol0", "pPol0", "+", "+", 0.04);
  return run;
}

inline RunInfo setup_2polExt_Lconstr_Pfixed(int energy, double lumi) {
  auto run = setup_2polExt_LPcnstr(energy, lumi);
  run.fix_pol("ePol-");
  run.fix_pol("ePol+");
  run.fix_pol("ePol0");
  run.fix_pol("pPol-");
  run.fix_pol("pPol+");
  run.fix_pol("pPol0");
  return run;
}

inline RunInfo setup_2polExt_Lfixed_Pconstr(int energy, double lumi) {
  auto run = setup_2polExt_LPcnstr(energy, lumi);
  run.fix_lumi();
  return run;
}

inline RunInfo setup_2polExt_LPfixed(int energy, double lumi) {
  auto run = setup_2polExt_Lconstr_Pfixed(energy, lumi);
  run.fix_lumi();
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

inline RunInfo setup_1pol_Lfixed_Pconstr(int energy, double lumi) {
  auto run = setup_1pol_LPcnstr(energy, lumi);
  run.fix_lumi();
  return run;
}

inline RunInfo setup_1pol_LPfixed(int energy, double lumi) {
  auto run = setup_1pol_Lconstr_Pfixed(energy, lumi);
  run.fix_lumi();
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

inline RunInfo setup_0pol_Lconstr_P0fixed(int energy, double lumi) {
  auto run = setup_0pol_LPcnstr(energy, lumi);
  run.fix_pol("ePol0");
  run.fix_pol("pPol0");
  return run;
}

inline RunInfo setup_0pol_Lfixed_P0constr(int energy, double lumi) {
  auto run = setup_0pol_LPcnstr(energy, lumi);
  run.fix_lumi();
  return run;
}

inline RunInfo setup_0pol_LPfixed(int energy, double lumi) {
  auto run = setup_0pol_Lconstr_P0fixed(energy, lumi);
  run.fix_lumi();
  return run;
}

// -----------------------------------------------------------------------------
// Available default setups as maps

using RunInfoFnc = std::function<RunInfo(int, double)>;
using RunInfoMap = std::map<std::string, RunInfoFnc>;

const std::map<std::string, RunInfoMap> default_run_setups{
    {"2pol",
     {{"2pol_LPcnstr", RunInfos::setup_2pol_LPcnstr},
      {"2pol_LPfixed", RunInfos::setup_2pol_LPfixed},
      {"2pol_Lconstr_Pfixed", RunInfos::setup_2pol_Lconstr_Pfixed},
      {"2pol_Lfixed_Pconstr", RunInfos::setup_2pol_Lfixed_Pconstr},
      {"2polExt_LPcnstr", RunInfos::setup_2polExt_LPcnstr},
      {"2polExt_LPfixed", RunInfos::setup_2polExt_LPfixed},
      {"2polExt_Lconstr_Pfixed", RunInfos::setup_2polExt_Lconstr_Pfixed},
      {"2polExt_Lfixed_Pconstr", RunInfos::setup_2polExt_Lfixed_Pconstr}}},
    {"1pol",
     {{"1pol_LPcnstr", RunInfos::setup_1pol_LPcnstr},
      {"1pol_LPfixed", RunInfos::setup_1pol_LPfixed},
      {"1pol_Lconstr_Pfixed", RunInfos::setup_1pol_Lconstr_Pfixed},
      {"1pol_LPcnstr_P0fixed", RunInfos::setup_1pol_LPcnstr_P0fixed},
      {"1pol_Lfixed_Pconstr", RunInfos::setup_1pol_Lfixed_Pconstr}}},
    {"0pol",
     {{"0pol_LPcnstr", RunInfos::setup_0pol_LPcnstr},
      {"0pol_LPfixed", RunInfos::setup_0pol_LPfixed},
      {"0pol_Lconstr_P0fixed", RunInfos::setup_0pol_Lconstr_P0fixed},
      {"0pol_Lfixed_P0constr", RunInfos::setup_0pol_Lfixed_P0constr}}}};

// -----------------------------------------------------------------------------

} // namespace RunInfos

#endif