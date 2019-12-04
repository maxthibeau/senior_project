import sys
from OpeningScreen import *
from SelectConfigFile import *
from SelectPFT import *
from SmoothOutliers import *
from DisplayRAMP import *
from DisplaySingleGraph import *
from ParameterChoosing import *
from ParameterDifference import *
from EnterRecoHyperparams import *
from NumericalSpinups import *
from SimulationStatistics import *

class Controller:

  def __init__(self):
    pass

  def show_opening_screen(self):
    self.opening_screen = OpeningScreen(self.show_config_file_selection, "Calibration Software")
    self.opening_screen.show()

  def show_config_file_selection(self):
    self.select_config_file = SelectConfigFile(self.show_pft_selection, "Select Configuration File")
    self.select_config_file.show()

  def show_pft_selection(self):
    self.select_pft = SelectPFT(self.show_gpp_outlier_smoothing, "Select Plant Functional Type")
    self.select_pft.show()

  def show_gpp_outlier_smoothing(self):
    self.smooth_gpp_outliers = SmoothOutliers(self.show_reco_outlier_smoothing, "Smooth GPP Outliers", "GPP")
    self.smooth_gpp_outliers.show()

  def show_reco_outlier_smoothing(self):
    self.smooth_reco_outliers = SmoothOutliers(self.show_gpp_ramp_funcs, "Smooth RECO Outliers", "RECO")
    self.smooth_reco_outliers.show()

  def show_gpp_ramp_funcs(self):
    self.display_gpp_ramp = DisplayRAMP(self.show_gpp_vs_emult, self.show_gpp_parameter_choosing, "GPP Ramp Functions", ["VPD", "SMRZ", "TMIN"], "GPP", "GPP Vs. Emult")
    self.display_gpp_ramp.show()

  def show_gpp_vs_emult(self):
    self.graph_gpp_vs_emult = DisplaySingleGraph(self.show_gpp_parameter_choosing, "GPP Vs. Emult")
    self.graph_gpp_vs_emult.show()

  def show_gpp_parameter_choosing(self):
    self.gpp_parameter_choosing = ParameterChoosing(self.show_gpp_parameter_difference, "Choose GPP Optimization Parameters", ["LUEmax", "VPDlow", "VPDhigh", "SMRZlow", "SMRZhigh", "TMINlow", "TMINhigh", "FT"])
    self.gpp_parameter_choosing.show()

  def show_gpp_parameter_difference(self):
    self.gpp_parameter_difference = ParameterDifference(self.redisplay_gpp_ramp_funcs, self.enter_reco_hyperparameters, "Differences in GPP Parameters After Optimization", self.gpp_parameter_choosing.parameters_to_optimize(), "GPP")
    self.gpp_parameter_difference.show()

  def redisplay_gpp_ramp_funcs(self):
    self.redisplay_gpp_ramp = DisplayRAMP(self.redisplay_gpp_vs_emult, self.enter_reco_hyperparameters, "GPP Ramp Functions", ["VPD", "SMRZ", "TMIN"], "GPP", "GPP Vs. Emult")
    self.redisplay_gpp_ramp.show()

  def redisplay_gpp_vs_emult(self):
    self.redisplay_gpp_vs_emult = DisplaySingleGraph(self.enter_reco_hyperparameters, "GPP Vs. Emult")
    self.redisplay_gpp_vs_emult.show()

  def enter_reco_hyperparameters(self):
    self.reco_hyperparameters = EnterRecoHyperparams(self.display_reco_ramp_funcs, "Enter RECO Optimization HyperParameters")
    self.reco_hyperparameters.show()

  def display_reco_ramp_funcs(self):
    self.plot_reco_ramps = DisplayRAMP(self.display_rh_over_c_vs_kmult, self.show_reco_parameter_choosing, "RECO Ramp Functions", ["TSOIL", "SMSF"], "RECO", "Rh/C Vs. Kmult")
    self.plot_reco_ramps.show()

  def display_rh_over_c_vs_kmult(self):
    self.display_rh_over_c_vs_kmult = DisplaySingleGraph(self.show_reco_parameter_choosing, "Rh/c vs. Kmult")
    self.display_rh_over_c_vs_kmult.show()

  def show_reco_parameter_choosing(self):
    self.reco_parameter_choosing = ParameterChoosing(self.show_reco_parameter_difference, "Choose RECO Optimization Parameters", ["Faut", "BTSOIL", "SMSFmin", "SMSFmax"])
    self.reco_parameter_choosing.show()

  def show_reco_parameter_difference(self):
    self.reco_parameter_difference = ParameterDifference(self.redisplay_reco_ramp_funcs, self.redisplay_reco_ramp_funcs, "Differences in RECO Parameters After Otimization", self.reco_parameter_choosing.parameters_to_optimize(), "RECO")
    self.reco_parameter_difference.show()

  def redisplay_reco_ramp_funcs(self):
    self.replot_reco_ramps = DisplayRAMP(self.redisplay_rh_over_c_vs_kmult, self.plot_soc_estimation, "RECO Ramp Functions", ["TSOIL", "SMSF"], "RECO", "Rh/C Vs. Kmult")
    self.replot_reco_ramps.show()

  def redisplay_rh_over_c_vs_kmult(self):
    self.redisplay_rh_over_c_vs_kmult = DisplaySingleGraph(self.plot_soc_estimation, "Rh/c vs. Kmult")
    self.redisplay_rh_over_c_vs_kmult.show()

  def plot_soc_estimation(self):
    self.plot_soc_estimation = DisplaySingleGraph(self.perform_numerical_spinups, "Estimated_SOC vs. Calculated_SOC")
    self.plot_soc_estimation.show()

  def perform_numerical_spinups(self):
    self.numerical_spinups = NumericalSpinups(self.show_simulation_statistics,"Numerical Spin-Up Iterations")
    self.numerical_spinups.show()

  def show_simulation_statistics(self):
    self.num_spins = SimulationStatistics(self.show_pft_selection,"Simulation Statistics",self.next_thing)
    self.num_spins.show()

  def next_thing(self):
    print ("next thing?")
    exit(1)

def main(argv):
  app = QtWidgets.QApplication(sys.argv)
  controller = Controller()
  controller.show_opening_screen()
  #controller.show_pft_selection()
  #controller.enter_reco_hyperparameters()
  #controller.plot_soc_estimation()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main(sys.argv)
