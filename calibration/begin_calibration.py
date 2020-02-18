import sys
from input_files import ConfigFile
from PFTSelector import *
from NewBPLUT import *
from FluxTowerData import *
from gpp import *
from funcs import *
import pandas as pd

def main(argv):
  if len(argv) < 1:
    print ("usage: <config file>")
    exit(1)
  config_fname = argv[0]
  config_file = ConfigFile(config_fname)
  meteor_input = config_file.meteorological_input()
  flux_tower_data = config_file.flux_tower_data()
  reference_input = config_file.reference_input()
  pft = PFTSelector.select_pft(meteor_input)

  tower_sites = meteor_input.sites_claimed_by_pft(pft)
  flux_lat_long = meteor_input.lat_long()
  flux_tower_data = flux_tower_data.set_coords(flux_lat_long)

  flux_tower_data_by_pft = flux_tower_data.take(tower_sites)
  print(reference_input.subset_data(['EC', 'frozen_area']))
  # meteor_tower_data_by_pft = meteor_input.take(tower_sites)
  # reference_data_by_pft = freference_data.take(tower_sites)

  tower_to_simulate = flux_tower_data_by_pft[0]
  df = pd.read_csv(tower_to_simulate)
  # fpar, par, 
  exit(1)
  # pft_data = PFT(pft_selected, meteor_input, reference_input)

  former_bplut = config_file.reference_bplut_table()
  former_bplut.load_current()
  # GPP
  VPD = 0.0 #GMAO FP
  SMRZ = 0.0 #SMAP L4SM
  TMIN = 0.0 #GMAO FP
  PAR = 0.0 #GMAO FP
  FPAR = 0.0 #MODIS/VIIRS
  gpp_calc = GPP(pft,former_bplut,VPD,SMRZ,TMIN,PAR,FPAR)
  former_bplut.after_optimization(pft,[2,5,8,10,11]) #CHANGE ARRAY
  #RECO
  Tsoil = 0.0 #SMAP L4SM
  SMSF = 0.0 #SMAP L4SM
  kmult_365 = 0.0 #from forward run
  npp_365 = 0.0 #from forward run
  reco_calc = reco.RECO(pft,former_bplut,gpp_calc,Tsoil,SMSF,kmult_365,npp_365)
  former_bplut.after_optimization(pft,[14,17,20]) #CHANGE ARRAY

if __name__ == "__main__":
  main(sys.argv[1:])
