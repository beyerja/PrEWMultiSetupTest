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

const std::string ReturnToZ_str = "81to101";
const std::string HighQ2_str = "180to275";

// -----------------------------------------------------------------------------

inline DifermionPars default_ReturnToZ() {
  // Default starting setup for return-to-Z mumu parametrisation
  // Using precise starting values
  return PrEWUtils::SetupHelp::DifermionPars()
      .s0("s0_2f_mu_" + ReturnToZ_str)
      .Ae("Ae_2f_mu_" + ReturnToZ_str, 0.21360014)
      .Af("Af_2f_mu_" + ReturnToZ_str, 0.20281099)
      .ef("ef_2f_mu_" + ReturnToZ_str, 0.01580906)
      .k0("k0_2f_mu_" + ReturnToZ_str, 0.07471141)
      .dk("dk_2f_mu_" + ReturnToZ_str, 0.00059199);
}

inline DifermionPars default_HighQ2() {
  // Default starting setup for high-Q^2 mumu parametrisation
  // Using precise starting values
  return PrEWUtils::SetupHelp::DifermionPars()
      .Ae(0.11251847)
      .Af(0.03217479)
      .ef(1.42594481)
      .k0(0.00033356)
      .dk(0.00031470);
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
    dif_par = dif_par.constr_Ae(dif_par.Ae_val, 0.0008);
  } else if (par_name == "Af") {
    dif_par = dif_par.constr_Af(dif_par.Af_val, 0.0008);
  } else if (par_name == "ef") {
    dif_par = dif_par.constr_ef(dif_par.ef_val, 0.0014);
  } else if (par_name == "k0") {
    dif_par = dif_par.constr_k0(dif_par.k0_val, 0.0013);
  } else if (par_name == "dk") {
    dif_par = dif_par.constr_dk(dif_par.dk_val, 0.0016);
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
    dif_par = dif_par.constr_Ae(dif_par.Ae_val, 0.0008);
  } else if (par_name == "Af") {
    dif_par = dif_par.constr_Af(dif_par.Af_val, 0.0006);
  } else if (par_name == "ef") {
    dif_par = dif_par.constr_ef(dif_par.ef_val, 0.0010);
  } else if (par_name == "k0") {
    dif_par = dif_par.constr_k0(dif_par.k0_val, 0.0010);
  } else if (par_name == "dk") {
    dif_par = dif_par.constr_dk(dif_par.dk_val, 0.0011);
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
  return std::make_pair(default_ReturnToZ().fix_k0().fix_dk(),
                        default_HighQ2().fix_k0().fix_dk());
}

inline DifParPair dif_pars_LEPconstr_Ae_Af() {
  auto mumu_ReturnToZ = default_ReturnToZ();
  auto mumu_HighQ2 = default_HighQ2();
  std::vector<std::string> constr_pars{"Ae", "Af"};
  for (const auto &constr_par : constr_pars) {
    mumu_ReturnToZ = LEP_constr_Zpole(mumu_ReturnToZ, constr_par);
  }
  return std::make_pair(mumu_ReturnToZ, mumu_HighQ2);
}

inline DifParPair dif_pars_LEPconstr_Ae_Af_fixed_ks() {
  auto mumu_ReturnToZ = default_ReturnToZ().fix_k0().fix_dk();
  auto mumu_HighQ2 = default_HighQ2().fix_k0().fix_dk();
  std::vector<std::string> constr_pars{"Ae", "Af"};
  for (const auto &constr_par : constr_pars) {
    mumu_ReturnToZ = LEP_constr_Zpole(mumu_ReturnToZ, constr_par);
  }
  return std::make_pair(mumu_ReturnToZ, mumu_HighQ2);
}

inline DifParPair dif_pars_ILCconstr_Ae_Af_ef_ks() {
  auto mumu_ReturnToZ = default_ReturnToZ();
  auto mumu_HighQ2 = default_HighQ2();
  std::vector<std::string> constr_pars{"Ae", "Af", "ef", "k0", "dk"};
  for (const auto &constr_par : constr_pars) {
    mumu_ReturnToZ = ILC_constr_Zpole(mumu_ReturnToZ, constr_par);
    mumu_HighQ2 = ILC_constr_HighQ2(mumu_HighQ2, constr_par);
  }
  return std::make_pair(mumu_ReturnToZ, mumu_HighQ2);
}

inline DifParPair dif_pars_ILCconstr_Ae_Af_ef_fixed_ks() {
  auto mumu_ReturnToZ = default_ReturnToZ().fix_k0().fix_dk();
  auto mumu_HighQ2 = default_HighQ2().fix_k0().fix_dk();
  std::vector<std::string> constr_pars{"Ae", "Af", "ef"};
  for (const auto &constr_par : constr_pars) {
    mumu_ReturnToZ = ILC_constr_Zpole(mumu_ReturnToZ, constr_par);
    mumu_HighQ2 = ILC_constr_HighQ2(mumu_HighQ2, constr_par);
  }
  return std::make_pair(mumu_ReturnToZ, mumu_HighQ2);
}

inline DifParPair dif_pars_AFB_k0_fixed_Ae_Af_dk() {
  /** Completely removes Af by fixing it to 0.
      Instead only uses unpolarised quantities AFB by proxy of ef.
      Ae and dk are fixed as well because there is no direct sensitivity to them 
      in an unpolarised dataset (keeping in mind that it's value does influence 
      the result on AFB and k0, but is fully correlated with the pol's).
      For truly correct result one needs to use constraints.
   **/
  auto mumu_ReturnToZ = default_ReturnToZ();
  auto AFB_rrZ =
      mumu_ReturnToZ.ef_val + 2 * mumu_ReturnToZ.Ae_val * mumu_ReturnToZ.Af_val;
  mumu_ReturnToZ = mumu_ReturnToZ.ef("AFB_2f_mu_" + ReturnToZ_str, AFB_rrZ)
                       .fix_Ae()
                       .fix_Af(0)
                       .fix_dk();

  auto mumu_HighQ2 = default_HighQ2();
  auto AFB_hQ2 =
      mumu_HighQ2.ef_val + 2 * mumu_HighQ2.Ae_val * mumu_HighQ2.Af_val;
  mumu_HighQ2 = mumu_HighQ2.ef("AFB_2f_mu_" + HighQ2_str, AFB_hQ2)
                    .fix_Ae()
                    .fix_Af(0)
                    .fix_dk();

  return std::make_pair(mumu_ReturnToZ, mumu_HighQ2);
}

// -----------------------------------------------------------------------------

} // namespace DifParPairs

#endif