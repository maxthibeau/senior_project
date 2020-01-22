import sys
from ConfigFile import *
from MeterologicalInput import *
from PFTSelector import *
import h5py

def main(argv):
  if len(argv) < 1:
    print ("usage: <config file>")
    exit(1)
  config_fname = argv[0]
  config_file = ConfigFile(config_fname)
  # FIXME: load meterological input dataset from config file
  fname = "../DataFiles/L4C_meteorological_input_dataset.h5"
  meteor_input = MeterologicalInput(h5py.File(fname, 'r'))
  pft_selected = PFTSelector.select_pft(meteor_input)

if __name__ == "__main__":
  main(sys.argv[1:])
