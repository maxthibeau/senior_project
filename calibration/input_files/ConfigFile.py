import h5py
import pandas as pd
from input_files.MeteorologicalInput import *
from input_files.FluxTowerData import *
from input_files.NewBPLUT import *
from input_files.ReferenceInput import *

class ConfigFile():

  def __init__(self, file_path):
    with open(file_path) as f:
      lines = [x.strip() for x in f.readlines() if not x.startswith("#")]
      self._reference_bplut_table, self._flux_tower_dir, self._flux_tower_sites_to_exclude, self._last_used_nature_run, self._meteorological_input, self._soc_input, self._output_hdf5_files = [x.strip() for x in lines]

      self._meteorological_input = MeteorologicalInput(self._meteorological_input)
      #FIXME: insert code that excludes tower sites
      self._flux_tower_data = FluxTowerData(self._flux_tower_dir)
      self._reference_bplut_table = NewBPLUT(self._reference_bplut_table)
      self._prev_simulation = ReferenceInput(self._last_used_nature_run)

      '''
      self._pfts = None
      self._opt_params = None
      lines = lines[6:]
      for x in lines:
        if x.startswith("PFT:"):
          self._pfts = x.split(":")[1]
          break
      for x in lines:
        if x.startswith("OPTPARAM:"):
          self._opt_params = x.split(":")[1]
          break
      '''

  def __str__(self):
    ret_str = ""
    ret_str += "reference_bplut_table: " + self._reference_bplut_table + "\n"
    ret_str += "flux_tower_sites: " + self._flux_tower_sites + "\n"
    ret_str += "flux_tower_sites_to_exclude" + self._flux_tower_sites_to_exclude + "\n"
    ret_str += "last_used_nature_run" + self._last_used_nature_run + "\n"
    ret_str += "input_hdf5_files: " + self._input_hdf5_files + "\n"
    ret_str += "output_hdf5_files: " + self._output_hdf5_files
    if self._pfts is not None:
      ret_str += "\nPFT:" + self._pfts
    if self._opt_params is not None:
      ret_str += "\nOPTPARAM:" + self._opt_params

    return ret_str

  def prev_simulation(self):
    return self._prev_simulation

  def reference_bplut_table(self):
    return self._reference_bplut_table

  def flux_tower_data(self):
    return self._flux_tower_data

  def flux_tower_sites_to_exclude(self):
    return self._flux_tower_sites_to_exclude

  def last_used_nature_run(self):
    return self._last_used_nature_run

  def meteorological_input(self):
    return self._meteorological_input

  def get_soc(self):
      # encoding = "ISO-8859-1"
      print("ACTUAL SOC: ")
      for line in open(self._soc_input, encoding = "ISO-8859-1"):
          print(line)

  def output_hdf5_files(self):
    return self._output_hdf5_files

  def pfts(self):
    return self._pfts

  def optimization_parameters(self):
    return self._opt_params



###########################################################################################
# TESTING #################################################################################
###########################################################################################

def _test_read():
  print("Test Read")
  fn = input("Enter the relative path of the config file:\n")
  cf = ConfigFile(fn)
  print()
  print(cf)
  return

def _test_write():
  print("Test Write")
  app = QApplication(sys.argv)
  ex = Maker()
  sys.exit(app.exec_())
  return

def main():
  print("The main is used for testing.")
  opt = input("1 to test reading, 2 to test writing\n")
  if opt == "1":
    _test_read()
  elif opt == "2":
    _test_write()
  else:
    main()

if __name__ == '__main__':
    main()


##########################################################################################
