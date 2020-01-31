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

  tower_site_indices = meteor_input.sites_claimed_by_pft(pft)

  flux_tower_data_for_pft = flux_tower_data.take(tower_site_indices)

  flux_tower_data.average_data_for_day(flux_tower_data_for_pft, 1, 3))
  former_bplut = config_file.reference_bplut_table()
  former_bplut.load_current()
  former_bplut.after_optimization(pft,[2,5,8,10,11]) #GPP

if __name__ == "__main__":
  main(sys.argv[1:])
