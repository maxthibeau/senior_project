import os
import csv
from affine import Affine
from gdal import osr
import numpy as np
import pandas as pd
from input_files.SingleFluxTower import *

class FluxTowerData():

  def __init__(self, flux_tower_dir):
    self._coordinates = [] # array of array of 2 elements [latitude, longitude]
    self._weights = [] # float calculated from coordinates
    self._fluxes = []
    self._non_missing_observations = []
    for filename in os.listdir(flux_tower_dir):
      filepath = flux_tower_dir + "/" + filename
      flux_tower = SingleFluxTower(filepath)
      self._non_missing_observations.append(flux_tower.non_missing_observations())
      self._fluxes.append(flux_tower)
    self._non_missing_observations = np.array(self._non_missing_observations)
    sample_flux_tower = self._fluxes[0]
    self._num_tower_vars = len(sample_flux_tower.tower_vars())
    # 365 day climatology, to be created later at the users request
    self._climatological_year = []

  def __getitem__(self, key):
    return self._fluxes[key]

  def subset_by_pft(self, tower_sites_claimed_by_pft):
    self._fluxes = [self._fluxes[site_index] for site_index in tower_sites_claimed_by_pft]
    self._weights = np.array([self._weights[site_index] for site_index in tower_sites_claimed_by_pft])
    self._coordinates = np.array([self._coordinates[site_index] for site_index in tower_sites_claimed_by_pft])
    self._non_missing_observations = np.array([self._non_missing_observations[site_index] for site_index in tower_sites_claimed_by_pft])

  def compute_climatological_year(self, start_date, end_date):
    # for every flux tower
    for flux_tower in self._fluxes:
      self._climatological_year.append(flux_tower.climatological_year(start_date, end_date))
    self._climatological_year = np.array(self._climatological_year)
    # format to be consistent with meteor input shape
    self._climatological_year = np.swapaxes(self._climatological_year, 0, 2)
    self._climatological_year = np.swapaxes(self._climatological_year, 0, 1)

  def gpp(self):
    return self._climatological_year[0]

  def reco(self):
    return self._climatological_year[1]

  def nee(self):
    return self._climatological_year[2]

  def weights(self):
    return self._weights

  def non_missing_observations(self):
    return self._non_missing_observations

  #resets flux tower data to include the coordinates
  def set_coords(self, coord_array):
    for i in range(len(self._fluxes)):
        self._coordinates.append(coord_array[i])
    self._coordinates = np.array(self._coordinates)
    for q in range(len(self._coordinates)):
        self._weights.append(0.0)
    self._set_weights()

  def _set_weights(self):
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
    self._weights = np.array(self._weights)
