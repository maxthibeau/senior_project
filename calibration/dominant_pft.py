import sys
import h5py
import numpy as np
from scipy import stats
from collections import defaultdict
from MeterologicalInput import *

def pft_to_claimed_sites(pft_grids, site_names):
  # a site is "claimed" by a pft when that pft is the dominant pft in that region
  pft_to_claimed_sites = defaultdict(list)
  print (pft_grids, site_names)
  for pft_grid, site_name in zip(pft_grids, site_names):     
    dominant_pfts = stats.mode(pft_grid)
    for dominant_pft in dominant_pfts:
      pft_to_claimed_sites[dominant_pft[0]].append(site_name)
  return pft_to_claimed_sites

def main(argv):
  if len(argv) < 1:
    print ("usage: <meterological_input_file.h5>")
    exit(1)
  fname = argv[0]
  meteor_input = MeterologicalInput(h5py.File(fname))
  print (pft_to_claimed_sites(meteor_input.pft_grids(), meteor_input.site_names()))

if __name__ == "__main__":
  main(sys.argv[1:])
