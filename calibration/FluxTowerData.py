import os
import csv
from affine import Affine
from gdal import osr
import numpy as np
#from SingleFluxTower import *

class FluxTowerData():

  def __init__(self, flux_tower_dir):
    self._coordinates = [] #array of array of 2 elements [latitude, longitude]
    self._weights = [] #float calculated from coordinates
    self._fluxes = []
    for filename in os.listdir(flux_tower_dir):
      filepath = flux_tower_dir + filename
      self._fluxes.append(filepath)
      #self._fluxes.append(SingleFluxTower(filepath))
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
    #print("*****coords******")
    for i in range(len(self._fluxes)):
        self._coordinates.append(coord_array[i])
        #print(i, coord_array[i])
    self._coordinates = np.array(self._coordinates)
    for q in range(len(self._coordinates)):
        self._weights.append(0.0)
    self._weights = self.set_weights()
    return self

  def set_weights(self):
    #World coordinates (longitude and latitude) to grid coordinates (EASE grid) to pixel coordinates (x,y)
    geotransform = (-17367530.45, 9000, 0, 7314540.83, 0, -9000) #x_min (lower bound of longitude), x_res (9000 is 9km), 0, y_max(upper bound of latitude), 0, y_res(same as x)
    worldGrid = Affine.from_gdal(*geotransform) #aka the EASE grid, worldGrid*(col,row) to return coords
    lat_long = osr.SpatialReference()
    #TODO: possible to change EPSG codes in config file
    lat_long.ImportFromEPSG(4326) #EPSG latlong code
    ease_grid = osr.SpatialReference()
    ease_grid.ImportFromEPSG(6933) #EPSG EASE-Grid 2.0 system code
    coord_to_ease = osr.CoordinateTransformation(lat_long,ease_grid) #from coordinates to ease grid coords
    pixel_coordinates = []
    for x in range(len(self._coordinates)):
        coord = self._coordinates[x] #coord[0] = long, coord[1] = lat
        change = coord_to_ease.TransformPoint(int(round(coord[1])),int(round(coord[0]))) #takes lat first, long second
        col_row = ~worldGrid * (change[0],change[1]) #outputs (x,y,z)
        col_row = (round(col_row[0],3),round(col_row[1],3))
        pixel_coordinates.append(col_row)
    for key in range(len(pixel_coordinates)):
        val = pixel_coordinates[key]
        lat = val[0]
        long = val[1]
        next = key+1
        same_grid = [] #composed of indices for tower weights
        same_grid.append(key)
        while(next < len(pixel_coordinates)):
            next_val = pixel_coordinates[next]
            if(next_val[0] <= (lat+1.5) and next_val[0] >= (lat-1.5) and next_val[1] <= (long+1.5) and next_val[1] >= (long-1.5)): #same 9-km latitude and longitude as the key
                if(self._weights[next] == 0.0 ): 
                    same_grid.append(next) #next is an index
            next += 1
        for i in range(len(same_grid)):
            tower = same_grid[i]
            if(self._weights[tower] == 0.0):
                self._weights[tower] = round(1/len(same_grid),3)
    print("WEIGHTS",self._weights)
