import numpy as np
import h5py
from collections import defaultdict
from scipy import stats

class MeteorologicalInput():

  def __init__(self, h5_fname):
    self._h5_file = h5py.File(h5_fname, 'r')
    self._pft_grids = self.subset_data(['ANC', 'lc_dom']).T
    self._site_names = self.subset_data(['SUBSET', 'site_name']).ravel()
    self._lat_long = self.subset_data(['SUBSET','site_latlon'])
    self._pfts = np.unique(self._pft_grids)
    self._pft_to_claimed_sites = self._find_pft_to_claimed_sites()

  def _find_pft_to_claimed_sites(self):
    # a site is "claimed" by a pft when that pft is the dominant pft in that region
    pft_to_claimed_sites = defaultdict(list)
    pft_grid_index = 0
    for pft_grid, in zip(self._pft_grids):
      dominant_pfts = stats.mode(pft_grid)[0]
      for dominant_pft in dominant_pfts:
        pft_to_claimed_sites[dominant_pft].append(pft_grid_index)
      pft_grid_index += 1
    return pft_to_claimed_sites

  def pfts(self,first,last):
    return self._pfts[first:last]

  def pft_grids(self):
    return self._pft_grids

  def site_names(self):
    return self._site_names

  def lat_long(self):
    return self._lat_long

  def subset_data(self, data_list):
    subsection = self._h5_file
    for request in data_list:
      subsection = subsection[request]
    return subsection[()]

  def subset_data_by_pft(self, data_list, pft, axis):
    data_to_subset = self.subset_data(data_list)
    indices_of_pft = self._pft_to_claimed_sites[pft]
    data_subsetted_by_pft = data_to_subset.take(indices = indices_of_pft, axis = axis)
    return data_subsetted_by_pft

  def sites_claimed_by_pft(self, pft):
    return self._pft_to_claimed_sites[int(pft)]
