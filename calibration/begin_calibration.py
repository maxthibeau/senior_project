import sys
from ConfigFile import *
from PFTSelector import *
from NewBPLUT import *
#import h5py

def main(argv):
  if len(argv) < 1:
    print ("usage: <config file>")
    exit(1)
  config_fname = argv[0]
  config_file = ConfigFile(config_fname)
  meteor_input = config_file.meteorological_input()
  pft_selected = PFTSelector.select_pft(meteor_input)
  #BPLUT Reference (FIXME: from actual config file)
  former_bplut = config_file.bplut()
  former_bplut.load_current()

if __name__ == "__main__":
  main(sys.argv[1:])
