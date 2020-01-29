import os
class FluxTowerData():

  def __init__(self, flux_tower_dir):
    for filename in os.listdir(flux_tower_dir):
      full_file_path = flux_tower_dir +'/'+ filename
      with open(full_file_path) as f:
        pass
