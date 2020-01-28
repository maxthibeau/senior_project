import sys
import h5py
from ConfigFile import *
from PFTSelector import *
from NewBPLUT import *


def main(argv):
  if len(argv) < 1:
    print ("usage: <config file>")
    exit(1)
  config_fname = argv[0]
  config_file = ConfigFile(config_fname)
  meteor_input = config_file.meteorological_input()

  pft_selected = PFTSelector.select_pft(meteor_input)

  former_bplut = config_file.reference_bplut_table()
  former_bplut.load_current()
  former_bplut.after_optimization(pft_selected,[2,5,8,10,11]) #GPP

if __name__ == "__main__":
  main(sys.argv[1:])
