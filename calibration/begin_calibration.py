import sys
from input_files.ConfigFile import *
import csv
from input_files import ConfigFile
from PFTSelector import *
from gpp import *
from reco import *
from Outliers import *
from datetime import date

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
  
  # TODO: prompt user for APAR bounds
  #outlier removal
  # outliers = Outliers(pft,flux_tower_data,reference_input)
  # outliers.display_outliers()
  gpp_calcs = GPP(pft, bplut, meteor_input, flux_tower_data)
  # reference_bplut.after_optimization(pft,[2,5,8,10,11]) #CHANGE ARRAY
  #RECO
  # Tsoil = meteor_input.subset_data_by_pft(['MET','tsoil'],pft,0) #meterological input MET (tsoil)
  # SMSF = meteor_input.subset_data_by_pft(['MET','smsf'],pft,0) #meterological input MET (smsf)
  kmult_365 = 0.0 #from forward run
  npp_365 = 0.0 #from forward run
  #reco_calcs = RECO(pft,bplut,gpp_calcs,Tsoil,SMSF,kmult_365,npp_365)
  #former_bplut.after_optimization(pft,[14,17,20]) #CHANGE ARRAY

if __name__ == "__main__":
  main(sys.argv[1:])
