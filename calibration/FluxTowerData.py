import os
import csv
import affine
import numpy as np
from SingleFluxTower import *

class FluxTowerData():

  def __init__(self, flux_tower_dir):
    self._coordinates = [] #array of array of 2 elements [latitude, longitude]
    self._weight = [] #float calculated from coordinates, should be 0.33 0.5 or 1
    self._fluxes = []
    for filename in os.listdir(flux_tower_dir):
      filepath = flux_tower_dir + filename
      self._fluxes.append(SingleFluxTower(filepath))
    self._fluxes = np.array(self._fluxes) 

  def __getitem__(self, key):
    return self._fluxes[key]

  def take(self, keys):
    return np.take(self._fluxes, keys)

  # day can take an int between 0 and 364
  @staticmethod
  def average_data_for_day(flux_towers, month, day):
    for flux_tower in flux_towers:
      df = flux_tower.data_frame()     
      rows = df.loc[(df['month'] == month) & (df['day'] == day)].to_numpy()
      print(rows)
      print(np.nanmean(rows, axis = 0))
      exit(1)

  #resets flux tower data to include the coordinates
  def set_coords(self, coord_array):
    for i in range(self._fluxes.size):
        self._coordinates.append(coord_array[i])
    self._coordinates = np.array(self._coordinates)
    #self._weights = self.set_weights()
    return self

  def set_weights(self):
    worldGrid = affine.Affine(self._coordinates)
    print(worldGrid)
    return worldGrid
