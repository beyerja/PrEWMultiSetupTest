#include "DifParPairs.h"
#include "RunInfos.h"

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
  std::string output_base = "../output/fit_results";

  std::vector<std::string> csv_input_files{
      "/nfs/dust/ilc/group/ild/beyerjac/TGCAnalysis/SampleProduction/"
      "NewMCProduction/2f_Z_l/PrEWInput/MuAcc_costheta_0.9925"};

  std::vector<std::string> distrs{"2f_mu_81to101_FZ", "2f_mu_81to101_BZ",
                                  "2f_mu_180to275"};

  spdlog::info("Defining run setups.");
  // clang-format off
  std::vector<double> luminosities {1e3, 2e3, 10e3};
  
  using RunInfoFnc = std::function<PrEWUtils::SetupHelp::RunInfo(int, double)>;
  std::map<std::string, RunInfoFnc> run_fncs {
    {"2pol_LPcnstr", RunInfos::setup_2pol_LPcnstr},
    {"2pol_LPfixed", RunInfos::setup_2pol_LPfixed},
    {"2pol_Lconstr_Pfixed", RunInfos::setup_2pol_Lconstr_Pfixed},
    {"1pol_LPcnstr", RunInfos::setup_1pol_LPcnstr},
    {"1pol_LPfixed", RunInfos::setup_1pol_LPfixed},
    {"1pol_Lconstr_Pfixed", RunInfos::setup_1pol_Lconstr_Pfixed},
    {"1pol_LPcnstr_P0fixed", RunInfos::setup_1pol_LPcnstr_P0fixed},
    {"0pol_LPcnstr", RunInfos::setup_0pol_LPcnstr},
    {"0pol_LPfixed", RunInfos::setup_0pol_LPfixed},
    {"0pol_Lconstr_P0fixed", RunInfos::setup_0pol_Lconstr_P0fixed}
  };
  
  
  
  std::map<std::string, bool> mu_acc_fixed {{"MuAccFree", false},
                                            {"MuAccFixd", true}};
  
  using DifParPairFnc = std::function<DifParPairs::DifParPair()>;
  std::map<std::string, DifParPairFnc> mumu_par_setups {
    {"mumu_free",     DifParPairs::dif_pars_free},
    {"mumu_fixed_ks", DifParPairs::dif_pars_fixed_ks},
    {"mumu_LEPconstr_Ae_Af_ef_ks", DifParPairs::dif_pars_LEPconstr_Ae_Af_ef_ks},
    {"mumu_LEPconstr_Ae_Af_ef_fixed_ks", DifParPairs::dif_pars_LEPconstr_Ae_Af_ef_fixed_ks},
    {"mumu_ILCconstr_Ae_Af_ef_ks", DifParPairs::dif_pars_ILCconstr_Ae_Af_ef_ks},
    {"mumu_ILCconstr_Ae_Af_ef_fixed_ks", DifParPairs::dif_pars_ILCconstr_Ae_Af_ef_fixed_ks}
  };
  // clang-format on

  spdlog::info("Start looping over setups.");
  for (const auto &[run_name, run_fnc] : run_fncs) {
    for (const auto &lumi : luminosities) {
      for (const auto &[mu_acc_name, fix_mu_acc] : mu_acc_fixed) {
        for (const auto &[mumu_par_name, mumu_par_fnc] : mumu_par_setups) {

          spdlog::info("Create setup.");
          PrEWUtils::Setups::GeneralSetup setup(energy);

          spdlog::info("Add files.");
          for (const auto &csv_file : csv_input_files) {
            setup.add_input_files(csv_file, ".*\\.csv", "CSV");
          }

          spdlog::info("Selecting distributions.");
          for (const auto &distr : distrs) {
            setup.use_distr(distr);
          }

          spdlog::info("Creating run info.");
          auto run = run_fnc(energy, lumi);
          setup.set_run(run);

          spdlog::info("Creating acceptance box (w/ polynomial) infos.");
          PrEWUtils::SetupHelp::AccBoxPolynomialInfo muon_box("MuonAcc");
          muon_box.add_distr("2f_mu_81to101_FZ");
          muon_box.add_distr("2f_mu_81to101_BZ");
          muon_box.add_distr("2f_mu_180to275");
          if (fix_mu_acc) {
            muon_box.fix_center();
            muon_box.fix_width();
          }
          setup.add(muon_box);

          // 7__________________________________________________________________
          spdlog::info("Setting up changes of the fit wrt. the toys.");
          PrEWUtils::Setups::FitModifier fit_modifier(energy);

          spdlog::info("Use generalised 2f parametrisation in fit.");
          auto mumu_par_pair = mumu_par_fnc();
          auto pars_mumu_81to101 = mumu_par_pair.first;
          auto pars_mumu_180to275 = mumu_par_pair.second;
          fit_modifier.add(PrEWUtils::SetupHelp::DifermionParamInfo(
              "2f_mu_81to101_FZ", pars_mumu_81to101));
          fit_modifier.add(PrEWUtils::SetupHelp::DifermionParamInfo(
              "2f_mu_81to101_BZ", pars_mumu_81to101));
          fit_modifier.add(PrEWUtils::SetupHelp::DifermionParamInfo(
              "2f_mu_180to275", pars_mumu_180to275));

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

          auto output_path = output_base + "_" + run_name + "_L" +
                             std::to_string(int(lumi)) + "_" + mu_acc_name +
                             +"_" + mumu_par_name + ".out";
          spdlog::info("Write results to: {}", output_path);
          PrEW::Output::Printer printer(output_path);
          printer.new_setup(energy, runner.get_data_connector());
          printer.add_fits(results);
          printer.write();

          spdlog::info("Single test done!");
        } // Loop mumu parameters
      }   // Loop muon acceptance
    }     // Loop luminosities
  }       // Loop run setups
  spdlog::info("All tests done!");
}

