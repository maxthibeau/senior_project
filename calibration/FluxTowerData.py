import os
import csv
import numpy as np

class FluxTowerData():

  def __init__(self, flux_tower_dir):
    self._fluxes = []
    for filename in os.listdir(flux_tower_dir):
      full_file_path = flux_tower_dir + filename
      self._fluxes.append(csv.reader(full_file_path))
    self._fluxes = np.array(self._fluxes)

  def __getitem__(self, key):
    return self._fluxes[key]

  def take(self, keys):
    return np.take(self._fluxes, keys)
