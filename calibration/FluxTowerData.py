import os
import csv
import affine
from gdal import osr
import numpy as np

class FluxTowerData():

  def __init__(self, flux_tower_dir):
    self._coordinates = [] #array of array of 2 elements [latitude, longitude]
    self._weight = [] #float calculated from coordinates, should be 0.33 0.5 or 1
    self._fluxes = []
    for filename in os.listdir(flux_tower_dir):
      full_file_path = flux_tower_dir + filename
      self._fluxes.append(csv.reader(full_file_path))
    self._fluxes = np.array(self._fluxes)

  def __getitem__(self, key):
    return self._fluxes[key]

  def take(self, keys):
    return np.take(self._fluxes, keys)

  #resets flux tower data to include the coordinates
  def set_coords(self, coord_array):
    for i in range(self._fluxes.size):
        self._coordinates.append(coord_array[i])
    self._coordinates = np.array(self._coordinates)
    #self._weights = self.set_weights()
    return self

  def set_weights(self):
    #World coordinates (longitude and latitude) to grid coordinates (EASE grid) to pixel coordinates (x,y)
    worldGrid = affine.Affine(self._coordinates)
    print(worldGrid)
    return worldGrid
