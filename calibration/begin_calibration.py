import sys
import h5py
from ConfigFile import *
from PFTSelector import *
from NewBPLUT import *
from FluxTowerData import *

def main(argv):
  if len(argv) < 1:
    print ("usage: <config file>")
    exit(1)
  config_fname = argv[0]
  config_file = ConfigFile(config_fname)
  meteor_input = config_file.meteorological_input()
  flux_tower_data = config_file.flux_tower_data()

  pft = PFTSelector.select_pft(meteor_input)

  tower_sites = meteor_input.sites_claimed_by_pft(pft)
  flux_lat_long = meteor_input.lat_long()
  flux_tower_data = flux_tower_data.set_coords(flux_lat_long)
  #print(flux_tower_data._coordinates)
  flux_tower_data_by_pft = flux_tower_data.take(tower_sites)


  # pft_data = PFT(pft_selected, meteor_input, reference_input)

  former_bplut = config_file.reference_bplut_table()
  former_bplut.load_current()
  former_bplut.after_optimization(pft,[2,5,8,10,11]) #GPP

if __name__ == "__main__":
  main(sys.argv[1:])
