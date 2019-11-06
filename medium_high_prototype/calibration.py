import sys
from OpeningScreen import *
from SelectConfigFile import *
from SelectPFT import *
from SmoothOutliers import *
from DisplayRAMP import *
from GPPVsEmult import *
from ParameterChoosing import *
from ParameterDifference import *

class Controller:

  def __init__(self):
    self.opening_screen = OpeningScreen(self.show_config_file_selection, "Calibration Software")

    self.select_config_file = SelectConfigFile(self.show_pft_selection, "Select Configuration File")

    self.select_pft = SelectPFT(self.show_gpp_outlier_smoothing, "Select Plant Functional Type")

    self.smooth_gpp_outliers = SmoothOutliers(self.show_reco_outlier_smoothing, "Smooth GPP Outliers", "GPP")

    self.smooth_reco_outliers = SmoothOutliers(self.show_gpp_ramp_funcs, "Smooth RECO Outliers", "RECO")

    self.display_gpp_ramp = DisplayRAMP(self.show_gpp_vs_emult, self.show_gpp_parameter_choosing, "GPP Ramp Functions", ["VPD", "SMRZ", "TMIN"], "GPP")

    self.graph_gpp_vs_emult = GPPVsEmult(self.show_gpp_parameter_choosing, "GPP Vs. Emult")

    self.gpp_parameter_choosing = ParameterChoosing(self.show_gpp_parameter_difference, "Choose GPP Optimization Parameters", ["LUEmax", "VPDlow", "VPDhigh", "SMRZlow", "SMRZhigh", "TMINlow", "TMINhigh", "FT"])

  def show_opening_screen(self):
    self.opening_screen.show()

  def show_config_file_selection(self):
    self.select_config_file.show()        

  def show_pft_selection(self):
    self.select_pft.show()

  def show_gpp_outlier_smoothing(self):
    self.smooth_gpp_outliers.show()

  def show_reco_outlier_smoothing(self):
    self.smooth_reco_outliers.show()

  def show_gpp_ramp_funcs(self):
    self.display_gpp_ramp.show()

  def show_gpp_vs_emult(self):
    self.graph_gpp_vs_emult.show()
  
  def show_gpp_parameter_choosing(self):
    self.gpp_parameter_choosing.show()

  def show_gpp_parameter_difference(self):
    self.gpp_parameter_difference = ParameterDifference(self.redisplay_gpp_ramp_funcs, self.next_thing, "Differences in GPP Parameters After Optimization", self.gpp_parameter_choosing.parameters_to_optimize(), "GPP")
    self.gpp_parameter_difference.show()

  def redisplay_gpp_ramp_funcs(self):
    print ("redisplayed")
    exit(1)
  def next_thing(self):
    print ("hoo yah")
    exit(1)

def main(argv):
  app = QtWidgets.QApplication(sys.argv)
  controller = Controller()
  controller.show_opening_screen()
  # controller.show_gpp_parameter_choosing()
  sys.exit(app.exec_())   

if __name__ == '__main__':
  main(sys.argv)
