import sys
from input_files.ConfigFile import *
import csv
from input_files import ConfigFile
from PFTSelector import *
from gpp import *
from reco import *
from soc import *
from Outliers import *
from datetime import date
#from PreliminarySpinUp import *
from scipy.optimize import minimize

#for Ubuntu (Windows) dispalys
#export DISPLAY=:0.0

def main(argv):
  if len(argv) < 1:
    print ("usage: <config file>")
    exit(1)

  # read in input files
  config_fname = argv[0]

  # while loop to allow continuation of optimizing for multiple PFTs
  pfts_optimized = []
  allow_pft = True
  updated = False
  while(allow_pft):
     #read in from config file
     config_file = ConfigFile.ConfigFile(config_fname)
     meteor_input = config_file.meteorological_input()
     flux_tower_data = config_file.flux_tower_data()
     reference_input = config_file.prev_simulation()
     if(updated): #check if the bplut has been optimized
         bplut = bplut
     else:
         bplut = config_file.reference_bplut_table()

     # assign coordinates to flux tower data
     flux_lat_long = meteor_input.lat_long()
     flux_tower_data.set_coords(flux_lat_long)

     # select a pft
     pft = int(PFTSelector.select_pft(meteor_input,pfts_optimized))

     # find tower sites claimed by pft
     tower_sites_claimed_by_pft = meteor_input.sites_claimed_by_pft(pft)

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
     gpp_optimizer.display_ramps()
     #gpp_optimizer.gpp_v_emult(pft, bplut, bplut.gpp_params(pft))
     simulated_gpp = gpp_optimizer.simulated_gpp()
     res = minimize(gpp_optimizer.func_to_optimize, bplut.gpp_params(pft)) #new optimized GPP parameter array
     print("*** PFT ",(pft+1), " ***")
     print("Number of Tower Sites that are PFT",(pft+1),"Dominant : ",len(flux_tower_data.towers()))
     #actual updating of GPP vals in BPLUT for pft
     bplut.after_optimization("GPP",pft,res.x)
     gpp_optimizer.display_optimized_ramps(pft,bplut)

     # RECO optimization process
     reco_optimizer = RECO(pft, bplut, simulated_gpp, meteor_input, flux_tower_data)
     reco_optimizer.display_ramps()
     #reco_optimizer.rhc_v_kmult()
     res = minimize(reco_optimizer.func_to_optimize, bplut.reco_params(pft)) #new optimized RECO parameter array
     #actual updating of RECO vals in BPLUT for pft
     bplut.after_optimization("RECO",pft,res.x)
     reco_optimizer.display_optimized_ramps(pft,bplut)

     #SOC calculation
     analytical_spin = AnalyticalModelSpinUp(reco_optimizer.get_kmult(), simulated_gpp, float(bplut[pft,'fmet']), float(bplut[pft,'fstr']), float(bplut[pft,'kopt']), float(bplut[pft,'kstr']), float(bplut[pft,'kslw']),float(bplut[pft,'fraut']))
     soc_calc = SOC(pft,bplut,flux_tower_data.towers(),analytical_spin.summed_kmults(),analytical_spin.get_npps(),flux_tower_data.socs())
     numerical_spin =  NumericalModelSpinUp(simulated_gpp, analytical_spin.summed_kmults(), soc_calc.get_litterfall(), pft, float(bplut[pft,'kopt']),float(bplut[pft,'kstr']), float(bplut[pft,'kslw']), float(bplut[pft,'fmet']), float(bplut[pft,'fstr']),float(bplut[pft,'fraut']), analytical_spin)
     #rmse on various statistics for pft

     #pfts optimized
     pfts_optimized.append(pft+1)

     try:
         choice = input("Would you like to optimize another PFT? (y/n): ").lower()
     except ValueError:
         choice = "xxx" #will cause to input another choice
     if(choice == "n"):
       allow_pft = False
     elif(choice == "y"):
       allow_pft = True
       updated = True
     else:
       print("Invalid value: please try again")

  #output config file
  #write input/reference data to config
  #write updated bplut to config file

  exit(1)

if __name__ == "__main__":
  main(sys.argv[1:])
