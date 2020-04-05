import sys
from GUI.OpeningScreen import *
from GUI.SelectConfigFile import *
from GUI.SelectPFT import *
from GUI.SmoothOutliers import *
from GUI.DisplayRAMP import *
from GUI.DisplaySingleGraph import *
from GUI.ParameterChoosing import *
from GUI.ParameterDifference import *
from GUI.EnterRecoHyperparams import *
from GUI.DisplaySOC import *
from GUI.NumericalSpinups import *
from GUI.SimulationStatistics import *
#from GUI.TopBarLayout import *

#for Mark's Ubuntu
#export DISPLAY=:0.0

class Controller:

  def __init__(self, width, height):
    self._tool_tips = self.readInDescriptions()
    self._opening_screen = OpeningScreen(width, height, "Calibration Software")
    self._opening_screen.move(250,20)
    self._select_config_file = SelectConfigFile(width, height, "Select Config File")
    self._select_config_file.move(250,20)
    self._pft_selection = SelectPFT(width, height, "Select Plant Functional Type",self._tool_tips)
    self._pft_selection.move(250,20)
    self._gpp_outlier_smoothing = SmoothOutliers(width, height, "Smooth GPP Outliers", "GPP",self._tool_tips)
    self._gpp_outlier_smoothing.move(250,20)
    self._reco_outlier_smoothing = SmoothOutliers(width, height, "Smooth RECO Outliers", "RECO",self._tool_tips)
    self._reco_outlier_smoothing.move(250,20)

    self._gpp_vs_emult = DisplaySingleGraph(width, height, "GPP vs. EMult")
    self._gpp_vs_emult.move(250,20)
    self._gpp_ramp_plots = DisplayRAMP(width, height, "GPP Ramp Functions", "GPP", ["VPD", "SMRZ", "TMIN"], self._gpp_vs_emult, "GPP vs. EMult")
    self._gpp_ramp_plots.move(250,20)
    self._select_gpp_opt_params = ParameterChoosing(width, height, "Choose GPP Optimization Parameters", ["LUEmax", "VPD_min", "VPD_max", "SMRZ_min", "SMRZ_max", "TMIN_min", "TMIN_max", "FT"], self._tool_tips, "GPP")
    self._select_gpp_opt_params.move(250,20)
    self._gpp_param_diff = ParameterDifference(width, height, "Difference in GPP Parameters After Optimization", self._select_gpp_opt_params.params_to_optimize(), "GPP", self._gpp_ramp_plots)
    self._gpp_param_diff.move(250,20)

    self._select_reco_hyperparams = EnterRecoHyperparams(width, height, "Enter RECO Optimization Hyperparameters")
    self._select_reco_hyperparams.move(250,20)
    self._rh_c_vs_k_mult = DisplaySingleGraph(width, height, "RH/C Vs. Kmult")
    self._rh_c_vs_k_mult.move(250,20)
    self._reco_ramp_funcs = DisplayRAMP(width, height, "RECO Ramp Functions", "RECO", ["TSOIL", "SMSF"], self._rh_c_vs_k_mult, "Rh/C Vs. Kmult")
    self._reco_ramp_funcs.move(250,20)
    self._reco_params_to_optimize = ParameterChoosing(width, height, "Choose RECO Optimization Parameters", ["Faut", "TSOIL", "SMSF_min", "SMSF_max"],self._tool_tips, "RECO")
    self._reco_params_to_optimize.move(250,20)
    self._reco_param_diff = ParameterDifference(width, height, "Difference in RECO Parameters After Optimization", self._reco_params_to_optimize.params_to_optimize(), "RECO", self._reco_ramp_funcs)
    self._reco_param_diff.move(250,20)
    self._plot_soc_estimation = DisplaySOC(width, height, "Estimated_SOC vs. Calculated_SOC")
    self._plot_soc_estimation.move(250,20)
    self._numerical_spinups = NumericalSpinups(width, height, "Numerical Spin-Up Iterations")
    self._numerical_spinups.move(250,20)
    self._post_spin_stats = SimulationStatistics(width, height, "Simulation Statistics")
    self._post_spin_stats.move(250,20)

    #set next and previous pages for certain screens
    self._opening_screen.set_next_page(self._select_config_file)

    self._select_config_file.set_prev_page(self._opening_screen)
    self._select_config_file.set_next_page(self._pft_selection)

    self._pft_selection.set_prev_page(self._select_config_file)
    self._pft_selection.set_next_page(self._gpp_outlier_smoothing)

    self._gpp_outlier_smoothing.set_prev_page(self._pft_selection)
    self._gpp_outlier_smoothing.set_next_page(self._reco_outlier_smoothing)

    self._reco_outlier_smoothing.set_prev_page(self._gpp_outlier_smoothing)
    self._reco_outlier_smoothing.set_next_page(self._gpp_ramp_plots)

    self._gpp_ramp_plots.set_prev_page(self._reco_outlier_smoothing)
    self._gpp_ramp_plots.set_next_page(self._select_gpp_opt_params)

    self._select_gpp_opt_params.set_prev_page(self._gpp_ramp_plots)
    self._select_gpp_opt_params.set_next_page(self._gpp_param_diff)

    self._gpp_param_diff.set_prev_page(self._select_gpp_opt_params)
    self._gpp_param_diff.set_next_page(self._select_reco_hyperparams)

    self._select_reco_hyperparams.set_prev_page(self._select_gpp_opt_params)
    self._select_reco_hyperparams.set_next_page(self._reco_ramp_funcs)

    self._reco_ramp_funcs.set_prev_page(self._select_reco_hyperparams)
    self._reco_ramp_funcs.set_next_page(self._reco_params_to_optimize)

    self._reco_params_to_optimize.set_prev_page(self._reco_ramp_funcs)
    self._reco_params_to_optimize.set_next_page(self._reco_param_diff)

    self._reco_param_diff.set_prev_page(self._reco_params_to_optimize)
    self._reco_param_diff.set_next_page(self._plot_soc_estimation)

    self._plot_soc_estimation.set_prev_page(self._reco_param_diff)
    self._plot_soc_estimation.set_next_page(self._numerical_spinups)

    self._numerical_spinups.set_prev_page(self._plot_soc_estimation)
    self._numerical_spinups.set_next_page(self._post_spin_stats)

    self._post_spin_stats.set_prev_page(self._numerical_spinups)
    self._post_spin_stats.set_next_page(self._pft_selection)

    self._opening_screen.show()

  def perform_numerical_spinups(self):
    self.numerical_spinups = NumericalSpinups(self.show_simulation_statistics,"Numerical Spin-Up Iterations")
    self.numerical_spinups.show()

  def show_simulation_statistics(self):
    self.num_spins = SimulationStatistics(self.show_pft_selection,"Simulation Statistics",self.next_thing)
    self.num_spins.show()

  def next_thing(self):
    print ("next thing?")
    exit(1)

  def current_window(self):
    return ("current window")

  def readInDescriptions(self):
      tooltipDict = {}
      with open("../DataFiles/varDescriptions.txt","r") as f:
          for line in f:
             if not line.startswith("#"):
                 line = line.split(":")
                 keys,vals = line[0],line[1].strip("\n")
                 tooltipDict[keys] = vals
      return tooltipDict

def main(argv):

  width = 800
  height = 600

  app = QtWidgets.QApplication(sys.argv)
  controller = Controller(width, height)
  sys.exit(app.exec_())

if __name__ == '__main__':
  main(sys.argv)
