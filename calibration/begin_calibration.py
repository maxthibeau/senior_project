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
  window = int(input("Please specify the number of days for the outlier smooting window size (whole number): "))
  flux_tower_data.smooth_gpp_outliers("gust", window)
  flux_tower_data.smooth_reco_outliers("gust", window)
  # flux_tower_data.display_gpp_smoothing(1)
  # flux_tower_data.display_reco_smoothing(1)

  # GPP optimization process
  gpp_optimizer = GPP(pft, bplut, meteor_input, flux_tower_data)
  simulated_gpp = gpp_optimizer.simulated_gpp()
  # gpp_optimizer.display_ramps()
  res = minimize(gpp_optimizer.func_to_optimize, bplut.gpp_params(pft))
  print(bplut.gpp_params(pft))
  print(res.x)
  # reference_bplut.after_optimization(pft,[2,5,8,10,11]) #CHANGE ARRAY
  #RECO
  reco_optimizer = RECO(pft, bplut, simulated_gpp, meteor_input, flux_tower_data)
  reco_optimizer.display_ramps()
  res = minimize(reco_optimizer.func_to_optimize, bplut.reco_params(pft))
  print(bplut.reco_params(pft))
  print(res.x)
  exit(1)
  #former_bplut.after_optimization(pft,[14,17,20]) #CHANGE ARRAY

if __name__ == "__main__":
  main(sys.argv[1:])
