import sys
from input_files.ConfigFile import *
import csv
from input_files import ConfigFile
from PFTSelector import *
from gpp import *
from reco import *
from Outliers import *
from datetime import date
from PreliminarySpinUp import *
from scipy.optimize import minimize

def main(argv):
  if len(argv) < 1:
    print ("usage: <config file>")
    exit(1)

  # read in input files
  config_fname = argv[0]
  config_file = ConfigFile.ConfigFile(config_fname)
  meteor_input = config_file.meteorological_input()
  flux_tower_data = config_file.flux_tower_data()
  reference_input = config_file.prev_simulation()
  bplut = config_file.reference_bplut_table()

  # while loop to allow continuation of optimizing for multiple PFTs
  allow_pft = True
  while(allow_pft):
     self.optimize() #to optimize at least once
     try:
         choice = toLower(input("Would you like to optimize another PFT? (y/n): "))
     except ValueError:
         choice = "xxx" #will cause to input another choice
     if(choice == "n"):
       allow_pft = False
     else if(choice == "y"):
       allow_pft = True
     else:
       print("Invalid value: please try again")

  exit(1)

  def optimize(self):
      # select a pft
      pft = int(PFTSelector.select_pft(meteor_input))

      # find tower sites claimed by pft
      tower_sites_claimed_by_pft = meteor_input.sites_claimed_by_pft(pft)

      # assign coordinates to flux tower data
      flux_lat_long = meteor_input.lat_long()
      flux_tower_data.set_coords(flux_lat_long)

      # subset data by pft
      flux_tower_data.subset_by_pft(tower_sites_claimed_by_pft)
      meteor_input.subset_by_pft(tower_sites_claimed_by_pft)
      reference_input.subset_by_pft(pft, tower_sites_claimed_by_pft)

      # compute climatological year
      climatology_start_date = datetime(2000, 1, 1)
      climatology_end_date = datetime(2014, 12, 31)
      meteor_input.compute_climatological_year(climatology_start_date, climatology_end_date)
      flux_tower_data.compute_climatological_year(climatology_start_date, climatology_end_date)

      # outlier removal and display
      flux_tower_data.smooth_outliers("gust")
      flux_tower_data.display_smoothing()

      # GPP optimization process
      gpp_optimizer = GPP(pft, bplut, meteor_input, flux_tower_data)
      simulated_gpp = gpp_optimizer.simulated_gpp()
      gpp_optimizer.display_ramps()
      res = minimize(gpp_optimizer.func_to_optimize, bplut.gpp_params(pft))
      print("*** PFT ",pft, " ***")
      print("GPP: ",bplut.gpp_params(pft))
      print(res.x)
      # reference_bplut.after_optimization(pft,[2,5,8,10,11]) #CHANGE ARRAY
      # RECO optimization process
      reco_optimizer = RECO(pft, bplut, simulated_gpp, meteor_input, flux_tower_data)
      reco_optimizer.display_ramps()
      res = minimize(reco_optimizer.func_to_optimize, bplut.reco_params(pft))
      print("RECO: ",bplut.reco_params(pft))
      print("res.x: ",res.x)
      #former_bplut.after_optimization(pft,[14,17,20]) #CHANGE ARRAY

if __name__ == "__main__":
  main(sys.argv[1:])
