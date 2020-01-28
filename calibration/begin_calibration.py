import sys
from ConfigFile import *
from MeterologicalInput import *
from PFTSelector import *
from NewBPLUT import *
#import h5py

def main(argv):
  if len(argv) < 1:
    print ("usage: <config file>")
    exit(1)
  config_fname = argv[0]
  #config_file = ConfigFile(config_fname)
  # FIXME: load meterological input dataset from config file
  # fname = "../DataFiles/L4C_meteorological_input_dataset.h5"
  # meteor_input = MeterologicalInput(h5py.File(fname, 'r'))
  # pft_selected = PFTSelector.select_pft(meteor_input)
  #BPLUT Reference (FIXME: from actual config file)
  bplut_ref = '../DataFiles/SMAP_BPLUT_2018'
  former_bplut = NewBPLUT(bplut_ref)
  former_bplut.load_current()

if __name__ == "__main__":
  main(sys.argv[1:])
