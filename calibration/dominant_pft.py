import sys
import h5py
import numpy as np
from scipy import stats
from collections import defaultdict

def pft_to_claimed_sites(pft_grids, site_names):
  poss_pfts = np.unique(pft_grids)
  # sites are stored in columns, transposing makes them stored in rows
  pft_grids = pft_grids.T
  # a site is "claimed" by a pft when that pft is the dominant pft in that region
  pft_to_claimed_sites = defaultdict(list)
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
  f = h5py.File(fname, 'r')
  pft_grids = f['ANC']['lc_dom'][()]
  site_names = f['SUBSET']['site_name'][()].ravel()
  print (pft_to_claimed_sites(pft_grids, site_names))

if __name__ == "__main__":
  main(sys.argv[1:])
