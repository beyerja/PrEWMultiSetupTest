#ifndef LIB_PREWMULTISETUPTEST_RUNPHSYICSCOMBS_H
#define LIB_PREWMULTISETUPTEST_RUNPHSYICSCOMBS_H 1

#include "DifParPairs.h"
#include "RunInfos.h"

// Standard library
#include <string>
#include <vector>

namespace RunPhysicsCombs {

// -----------------------------------------------------------------------------

using DifParPairFnc = std::function<DifParPairs::DifParPair()>;
using RunInfoFnc = std::function<PrEWUtils::SetupHelp::RunInfo(int, double)>;

struct RunPhysicsCombs {
  /** Specify which runs will use which physics parameters.
   **/
  std::map<std::string, RunInfoFnc> run_fncs{};
  std::map<std::string, DifParPairFnc> mumu_par_setups{};
};
using RunPhysicsCombVec = std::vector<RunPhysicsCombs>;

// -----------------------------------------------------------------------------

// clang-format off
RunPhysicsCombs comb_2pol {
  { {"2pol_LPcnstr", RunInfos::setup_2pol_LPcnstr},
    {"2pol_LPfixed", RunInfos::setup_2pol_LPfixed},
    {"2pol_Lconstr_Pfixed", RunInfos::setup_2pol_Lconstr_Pfixed},
    {"2pol_Lconstr_Pfixed", RunInfos::setup_2pol_Lconstr_Pfixed},
    {"2pol_Lconstr_Pfixed", RunInfos::setup_2pol_Lconstr_Pfixed},
    {"2pol_Lfixed_Pconstr", RunInfos::setup_2pol_Lfixed_Pconstr},
    {"2polExt_LPcnstr", RunInfos::setup_2polExt_LPcnstr},
    {"2polExt_LPfixed", RunInfos::setup_2polExt_LPfixed},
    {"2polExt_Lconstr_Pfixed", RunInfos::setup_2polExt_Lconstr_Pfixed},
    {"2polExt_Lfixed_Pconstr", RunInfos::setup_2polExt_Lfixed_Pconstr} },
  { {"mumu_free",     DifParPairs::dif_pars_free},
    {"mumu_fixed_ks", DifParPairs::dif_pars_fixed_ks},
    {"mumu_LEPconstr_Ae_Af_ks", DifParPairs::dif_pars_LEPconstr_Ae_Af},
    {"mumu_LEPconstr_Ae_Af_fixed_ks", DifParPairs::dif_pars_LEPconstr_Ae_Af_fixed_ks} } };

RunPhysicsCombs comb_1pol {
  { {"1pol_LPcnstr", RunInfos::setup_1pol_LPcnstr},
    {"1pol_LPfixed", RunInfos::setup_1pol_LPfixed},
    {"1pol_Lconstr_Pfixed", RunInfos::setup_1pol_Lconstr_Pfixed},
    {"1pol_LPcnstr_P0fixed", RunInfos::setup_1pol_LPcnstr_P0fixed},
    {"1pol_Lfixed_Pconstr", RunInfos::setup_1pol_Lfixed_Pconstr} },
  { {"mumu_free",     DifParPairs::dif_pars_free},
    {"mumu_fixed_ks", DifParPairs::dif_pars_fixed_ks},
    {"mumu_LEPconstr_Ae_Af_ks", DifParPairs::dif_pars_LEPconstr_Ae_Af},
    {"mumu_LEPconstr_Ae_Af_fixed_ks", DifParPairs::dif_pars_LEPconstr_Ae_Af_fixed_ks} } };

RunPhysicsCombs comb_0pol {
  { {"0pol_LPcnstr", RunInfos::setup_0pol_LPcnstr},
    {"0pol_LPfixed", RunInfos::setup_0pol_LPfixed},
    {"0pol_Lconstr_P0fixed", RunInfos::setup_0pol_Lconstr_P0fixed},
    {"0pol_Lfixed_P0constr", RunInfos::setup_0pol_Lfixed_P0constr} },
  { {"mumu_ILCconstr_Ae_Af_ef_ks", DifParPairs::dif_pars_ILCconstr_Ae_Af_ef_ks},
    {"mumu_ILCconstr_Ae_Af_ef_fixed_ks", DifParPairs::dif_pars_ILCconstr_Ae_Af_ef_fixed_ks} } };
// clang-format on

// -----------------------------------------------------------------------------

} // namespace RunPhysicsCombs

#endif