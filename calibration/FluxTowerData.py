import os
import csv
class FluxTowerData():

  def __init__(self, flux_tower_dir):
    fluxes = []
    for filename in os.listdir(flux_tower_dir):
      full_file_path = flux_tower_dir + filename
      fluxes.append(csv.reader(full_file_path))

  def __getitem__(self, key):
    return fluxes[key]
