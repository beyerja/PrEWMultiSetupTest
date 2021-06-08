#ifndef LIB_PREWRUNEXAMPLE_DIFPARPAIRS_H
#define LIB_PREWRUNEXAMPLE_DIFPARPAIRS_H 1

// Includes from PrEWUtils
#include "SetupHelp/SetupInfos.h"

// Standard library
#include <stdexcept>
#include <string>

using namespace PrEWUtils::SetupHelp;

namespace DifParPairs {

// -----------------------------------------------------------------------------

using DifParPair = std::pair<PrEWUtils::SetupHelp::DifermionPars,
                             PrEWUtils::SetupHelp::DifermionPars>;

// -----------------------------------------------------------------------------

inline DifermionPars default_ReturnToZ() {
  // Default starting setup for return-to-Z mumu parametrisation
  // Using precise starting values
  return PrEWUtils::SetupHelp::DifermionPars()
      .s0("s0_2f_mu_81to101")
      .Ae("Ae_2f_mu_81to101", 0.21360014)
      .Af("Af_2f_mu_81to101", 0.20281099)
      .ef("ef_2f_mu_81to101", 0.01580906)
      .kL("kL_2f_mu_81to101", 0.03765170)
      .kR("kR_2f_mu_81to101", 0.03705971);
}

inline DifermionPars default_HighQ2() {
  // Default starting setup for high-Q^2 mumu parametrisation
  // Using precise starting values
  return PrEWUtils::SetupHelp::DifermionPars()
      .Ae(0.11251847)
      .Af(0.03217479)
      .ef(1.42594481)
      .kL(0.00032413)
      .kR(0.00000943);
}

// -----------------------------------------------------------------------------

inline DifermionPars LEP_constr_Zpole(DifermionPars dif_par,
                                      const std::string &par_name) {
  // LEP/SLC-like constraints at the Z pole (rounded somewhat optimistic)
  if (par_name == "s0") {
    dif_par = dif_par.constr_s0(dif_par.s0_val, 1.e-3);
  } else if (par_name == "Ae") {
    dif_par = dif_par.constr_Ae(dif_par.Ae_val, 1.e-3);
  } else if (par_name == "Af") {
    dif_par = dif_par.constr_Af(dif_par.Af_val, 1.e-2);
  } else if (par_name == "ef") {
    dif_par = dif_par.constr_ef(dif_par.ef_val, 1.e-2);
  } else if (par_name == "kL") {
    dif_par = dif_par.constr_kL(dif_par.kL_val, 1.e-2);
  } else if (par_name == "kR") {
    dif_par = dif_par.constr_kR(dif_par.kR_val, 1.e-2);
  } else {
    throw std::invalid_argument(par_name + " isn't valid 2f parameter.");
  }
  return dif_par;
}

inline DifermionPars LEP_constr_HighQ2(DifermionPars dif_par,
                                       const std::string &par_name) {
  // LEP/SLC-like constraints at high energies
  // -> No actual results (Except s0 and AFB at diverse energies)
  // => Assume somewhat optimistic constraints
  if (par_name == "s0") {
    dif_par = dif_par.constr_s0(dif_par.s0_val, 1.e-2);
  } else if (par_name == "Ae") {
    dif_par = dif_par.constr_Ae(dif_par.Ae_val, 5.e-2);
  } else if (par_name == "Af") {
    dif_par = dif_par.constr_Af(dif_par.Af_val, 5.e-2);
  } else if (par_name == "ef") {
    dif_par = dif_par.constr_ef(dif_par.ef_val, 5.e-2);
  } else if (par_name == "kL") {
    dif_par = dif_par.constr_kL(dif_par.kL_val, 5.e-2);
  } else if (par_name == "kR") {
    dif_par = dif_par.constr_kR(dif_par.kR_val, 5.e-2);
  } else {
    throw std::invalid_argument(par_name + " isn't valid 2f parameter.");
  }
  return dif_par;
}

inline DifermionPars ILC_constr_Zpole(DifermionPars dif_par,
                                      const std::string &par_name) {
  // ILC-like constraints at the Z pole from return-to-Z
  if (par_name == "s0") {
    throw std::invalid_argument("ILC s0 constraint depends on lumimeter.");
  } else if (par_name == "Ae") {
    dif_par = dif_par.constr_Ae(dif_par.Ae_val, 0.0006);
  } else if (par_name == "Af") {
    dif_par = dif_par.constr_Af(dif_par.Af_val, 0.00038);
  } else if (par_name == "ef") {
    dif_par = dif_par.constr_ef(dif_par.ef_val, 0.0007);
  } else if (par_name == "kL") {
    dif_par = dif_par.constr_kL(dif_par.kL_val, 0.0006);
  } else if (par_name == "kR") {
    dif_par = dif_par.constr_kR(dif_par.kR_val, 0.0007);
  } else {
    throw std::invalid_argument(par_name + " isn't valid 2f parameter.");
  }
  return dif_par;
}

inline DifermionPars ILC_constr_HighQ2(DifermionPars dif_par,
                                       const std::string &par_name) {
  // ILC-like constraints at high energies
  if (par_name == "s0") {
    throw std::invalid_argument("ILC s0 constraint depends on lumimeter.");
  } else if (par_name == "Ae") {
    dif_par = dif_par.constr_Ae(dif_par.Ae_val, 0.0006);
  } else if (par_name == "Af") {
    dif_par = dif_par.constr_Af(dif_par.Af_val, 0.00026);
  } else if (par_name == "ef") {
    dif_par = dif_par.constr_ef(dif_par.ef_val, 0.00045);
  } else if (par_name == "kL") {
    dif_par = dif_par.constr_kL(dif_par.kL_val, 0.00042);
  } else if (par_name == "kR") {
    dif_par = dif_par.constr_kR(dif_par.kR_val, 0.00049);
  } else {
    throw std::invalid_argument(par_name + " isn't valid 2f parameter.");
  }
  return dif_par;
}

// -----------------------------------------------------------------------------

inline DifParPair dif_pars_free() {
  return std::make_pair(default_ReturnToZ(), default_HighQ2());
}

inline DifParPair dif_pars_fixed_ks() {
  return std::make_pair(default_ReturnToZ().fix_kL().fix_kR(),
                        default_HighQ2().fix_kL().fix_kR());
}

inline DifParPair dif_pars_LEPconstr_Ae_Af_ef_ks() {
  auto mumu_ReturnToZ = default_ReturnToZ();
  auto mumu_HighQ2 = default_HighQ2();
  std::vector<std::string> constr_pars{"Ae", "Af", "ef", "kL", "kR"};
  for (const auto &constr_par : constr_pars) {
    mumu_ReturnToZ = LEP_constr_Zpole(mumu_ReturnToZ, constr_par);
    mumu_HighQ2 = LEP_constr_HighQ2(mumu_HighQ2, constr_par);
  }
  return std::make_pair(mumu_ReturnToZ, mumu_HighQ2);
}

inline DifParPair dif_pars_LEPconstr_Ae_Af_ef_fixed_ks() {
  auto mumu_ReturnToZ = default_ReturnToZ().fix_kL().fix_kR();
  auto mumu_HighQ2 = default_HighQ2().fix_kL().fix_kR();
  std::vector<std::string> constr_pars{"Ae", "Af", "ef"};
  for (const auto &constr_par : constr_pars) {
    mumu_ReturnToZ = LEP_constr_Zpole(mumu_ReturnToZ, constr_par);
    mumu_HighQ2 = LEP_constr_HighQ2(mumu_HighQ2, constr_par);
  }
  return std::make_pair(mumu_ReturnToZ, mumu_HighQ2);
}

inline DifParPair dif_pars_ILCconstr_Ae_Af_ef_ks() {
  auto mumu_ReturnToZ = default_ReturnToZ();
  auto mumu_HighQ2 = default_HighQ2();
  std::vector<std::string> constr_pars{"Ae", "Af", "ef", "kL", "kR"};
  for (const auto &constr_par : constr_pars) {
    mumu_ReturnToZ = ILC_constr_Zpole(mumu_ReturnToZ, constr_par);
    mumu_HighQ2 = ILC_constr_HighQ2(mumu_HighQ2, constr_par);
  }
  return std::make_pair(mumu_ReturnToZ, mumu_HighQ2);
}

inline DifParPair dif_pars_ILCconstr_Ae_Af_ef_fixed_ks() {
  auto mumu_ReturnToZ = default_ReturnToZ().fix_kL().fix_kR();
  auto mumu_HighQ2 = default_HighQ2().fix_kL().fix_kR();
  std::vector<std::string> constr_pars{"Ae", "Af", "ef"};
  for (const auto &constr_par : constr_pars) {
    mumu_ReturnToZ = ILC_constr_Zpole(mumu_ReturnToZ, constr_par);
    mumu_HighQ2 = ILC_constr_HighQ2(mumu_HighQ2, constr_par);
  }
  return std::make_pair(mumu_ReturnToZ, mumu_HighQ2);
}

// -----------------------------------------------------------------------------

} // namespace DifParPairs

#endif