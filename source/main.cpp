#include "Definitions/DifParPairs.h"
#include "Definitions/RunInfos.h"

// Includes from PrEW
#include "GlobalVar/Chiral.h"
#include "Output/Printer.h"

// Includes from PrEWUtils
#include "Runners/ParallelRunner.h"
#include "SetupHelp/SetupInfos.h"
#include "Setups/FitModifier.h"
#include "Setups/GeneralSetup.h"

// Standard library
#include <string>

#include "spdlog/spdlog.h"

int main(int /*argc*/, char ** /*argv*/) {
  spdlog::set_level(spdlog::level::info);

  int energy = 250;
  int n_threads = 10;
  int n_toys = 300;
  std::string minuit_minimizers = "Combined(1000000,1000000,0.01)";
  std::string prew_minimizer = "PoissonNLL";
  std::string output_base = "../output/run_outputs/fit_results";

  std::vector<std::string> csv_input_files{
      "/nfs/dust/ilc/group/ild/beyerjac/TGCAnalysis/SampleProduction/"
      "NewMCProduction/2f_Z_l/PrEWInput/MuAcc_costheta_0.9925",
      "/nfs/dust/ilc/group/ild/beyerjac/TGCAnalysis/SampleProduction/"
      "NewMCProduction/4f_WW_sl/PrEWInput"};

  std::vector<std::string> distrs_2f{"2f_mu_81to101_FZ", "2f_mu_81to101_BZ",
                                     "2f_mu_180to275"};
  std::vector<std::string> distrs_WW{"WW_muminus", "WW_muplus"};

  spdlog::info("Defining run setups.");

  // Common to all runs
  std::vector<double> luminosities{1e3, 2e3, 10e3};

  // Figure out all potential options setups
  struct FullRunPhysSetup {
    // Helper struct that keeps track of all options
    std::string run_name{};
    RunInfos::RunInfoFnc run_fnc{};
    double lumi{};
    bool fix_mu_acc{};

    bool use_WW{};
    bool use_mumu{};

    std::string mumu_par_name{};
    DifParPairs::DifParPairFnc mumu_fnc{};

    bool use_WW_TGCs{};
    bool fix_WW_xs0{};
    bool fix_WW_A{};

    std::string output_name(const std::string &base) const {
      /** Define how the output file is supposed to be called, depending on all
          the options in this setup.
       **/
      std::string result =
          base + "_" + run_name + "_L" + std::to_string(int(lumi));

      if (fix_mu_acc) {
        result += "_MuAccFixd";
      } else {
        result += "_MuAccFree";
      }

      if (use_mumu) {
        result += "_" + mumu_par_name;
      }

      if (use_WW) {
        result += "_WW";

        if (use_WW_TGCs) {
          result += "cTGCs";
        } else {
          result += "";
      }

      if (fix_WW_xs0) {
        result += "_xs0Fixd";
      } else {
        result += "_xs0Free";
      }

      if (fix_WW_A) {
        result += "_AFixd";
      } else {
        result += "_AFree";
      }
    }

    result += ".out";
    return result;
  }
};

std::vector<FullRunPhysSetup> run_phys_setups{};

// Loop over all potential options to figure out all combinations to test
for (const auto &[run_cat, run_cat_map] : RunInfos::default_run_setups) {
  for (const auto &[run_name, run_fnc] : run_cat_map) {
    for (double lumi : luminosities) {
      for (bool use_WW : {true, false}) {

        std::vector<bool> fix_WW_pars = {true, false};
        if (!use_WW) {
          // If not using WW final state then don't test fixing WW pars
          fix_WW_pars = {false};
        }

        for (auto use_WW_TGCs : fix_WW_pars) {
          for (auto fix_WW_xs0 : fix_WW_pars) {
            for (auto fix_WW_A : fix_WW_pars) {

              for (bool use_mumu : {true, false}) {

                auto dif_par_map = DifParPairs::default_dif_pars.at(run_cat);
                if (!use_mumu) {
                  // If not using mumu final state, only have one fake item to
                  // loop
                  dif_par_map = {{"", {}}};
                }

                for (const auto &[mumu_par_name, mumu_fnc] : dif_par_map) {

                  for (bool fix_mu_acc : {true, false}) {

                    if (!(use_WW || use_mumu)) {
                      continue;
                    }

                    FullRunPhysSetup new_setup{
                        run_name,    run_fnc,    lumi,          fix_mu_acc,
                        use_WW,      use_mumu,   mumu_par_name, mumu_fnc,
                        use_WW_TGCs, fix_WW_xs0, fix_WW_A};
                    run_phys_setups.push_back(new_setup);

                  } // Loop muon acceptance fixed or free
                }   // Loop mumu setup
              }     // Loop use_mumu
            }       // Loop fixing WW A
          }         // Loop fixing WW xs0
        }           // Loop use WW TGCs
      }             // Loop use_WW
    }               // Loop collider setups
  }                 // Loop luminosities
} // Loop collider setup categories

spdlog::info("Start looping over setups.");
for (const auto &rps : run_phys_setups) {
  spdlog::info("Create setup.");
  PrEWUtils::Setups::GeneralSetup setup(energy);

  spdlog::info("Add files.");
  for (const auto &csv_file : csv_input_files) {
    setup.add_input_files(csv_file, ".*\\.csv", "CSV");
  }

  spdlog::info("Determining distributions.");
  std::vector<std::string> distrs{};
  if (rps.use_mumu) {
    distrs.insert(distrs.end(), distrs_2f.begin(), distrs_2f.end());
  }
  if (rps.use_WW) {
    distrs.insert(distrs.end(), distrs_WW.begin(), distrs_WW.end());
  }

  spdlog::info("Selecting distributions.");
  for (const auto &distr : distrs) {
    setup.use_distr(distr);
  }

  spdlog::info("Creating run info.");
  auto run = rps.run_fnc(energy, rps.lumi);
  setup.set_run(run);

  spdlog::info("Creating acceptance box (w/ polynomial) infos.");
  PrEWUtils::SetupHelp::AccBoxPolynomialInfo muon_box("MuonAcc");
  for (const auto &distr : distrs) {
    muon_box.add_distr(distr);
  }
  if (rps.fix_mu_acc) {
    muon_box.fix_center();
    muon_box.fix_width();
  }
  setup.add(muon_box);

  spdlog::info("Adding physics infos.");

  if (rps.use_WW) {
    if (rps.use_WW_TGCs) {
      spdlog::info("Creating TGC info.");
      PrEWUtils::SetupHelp::TGCInfo cTGC_info({"WW_muplus", "WW_muminus"},
                                              "quadratic");
      setup.add(cTGC_info);
    }

    spdlog::info("Creating WW chiral cross section infos.");
    PrEWUtils::SetupHelp::CrossSectionInfo xs_WW_muminus(
        "WW_muminus",
        {PrEW::GlobalVar::Chiral::eLpR, PrEW::GlobalVar::Chiral::eRpL});
    PrEWUtils::SetupHelp::CrossSectionInfo xs_WW_muplus(
        "WW_muplus",
        {PrEW::GlobalVar::Chiral::eLpR, PrEW::GlobalVar::Chiral::eRpL});

    if (!rps.fix_WW_xs0) {
      xs_WW_muminus.use_total_chiral_cross_section();
      xs_WW_muplus.use_total_chiral_cross_section();
    }
    if (!rps.fix_WW_A) {
      xs_WW_muminus.use_chiral_asymmetries();
      xs_WW_muplus.use_chiral_asymmetries();
    }

    setup.add(xs_WW_muminus);
    setup.add(xs_WW_muplus);
  }

  // 7__________________________________________________________________
  spdlog::info("Setting up changes of the fit wrt. the toys.");
  PrEWUtils::Setups::FitModifier fit_modifier(energy);

  if (rps.use_mumu) {
    spdlog::info("Use generalised 2f parametrisation in fit.");
    auto mumu_par_pair = rps.mumu_fnc();
    auto pars_mumu_81to101 = mumu_par_pair.first;
    auto pars_mumu_180to275 = mumu_par_pair.second;
    bool polarised = (rps.mumu_par_name != "mumu_unpol");
    fit_modifier.add(PrEWUtils::SetupHelp::DifermionParamInfo(
        "2f_mu_81to101_FZ", pars_mumu_81to101, polarised));
    fit_modifier.add(PrEWUtils::SetupHelp::DifermionParamInfo(
        "2f_mu_81to101_BZ", pars_mumu_81to101, polarised));
    fit_modifier.add(PrEWUtils::SetupHelp::DifermionParamInfo(
        "2f_mu_180to275", pars_mumu_180to275, polarised));
  }

  // 7__________________________________________________________________
  spdlog::info("Finalizing linking info.");
  setup.complete_setup(); // This must come last in linking setup

  spdlog::info("Create runner (incl. setting up toy generator).");
  PrEWUtils::Runners::ParallelRunner runner(setup, minuit_minimizers,
                                            prew_minimizer);

  spdlog::info("Performing instructed fit modifications.");
  runner.modify_fit(fit_modifier);

  spdlog::info("Run toys.");
  auto results = runner.run_toy_fits(energy, n_toys, n_threads);

  spdlog::info("All threads done, printing first result.");
  spdlog::info(results.at(0));

  auto output_path = rps.output_name(output_base);
  spdlog::info("Write results to: {}", output_path);
  PrEW::Output::Printer printer(output_path);
  printer.new_setup(energy, runner.get_data_connector());
  printer.add_fits(results);
  printer.write();

  spdlog::info("Single test done!");

} // Loop over full setups

spdlog::info("All tests done!");
}
