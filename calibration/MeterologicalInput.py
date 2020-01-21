import numpy as np

class MeterologicalInput():
  
  def __init__(self, h5_file):
    self._pft_grids = h5_file['ANC']['lc_dom'][()].T
    self._site_names = h5_file['SUBSET']['site_name'][()].ravel()
    self._pfts = np.unique(self._pft_grids)

  def pfts(self):
    return self._pfts          

  def pft_grids(self):
    return self._pft_grids

  def site_names(self):
    return self._site_names
