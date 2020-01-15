import sys
class ConfigFile():

  def __init__(self, file_path):
     with open(file_path) as f:
      self._reference_bplut_table, self._flux_tower_sites, self._flux_tower_sites_to_exclude, self._last_used_nature_run, self._input_hdf5_files, self._output_hdf5_files = [x.strip() for x in f.readlines()] 

  def __str__(self):
    print (self._input_hdf5_files)
    ret_str = ""
    ret_str += "reference_bplut_table: " + self._reference_bplut_table + "\n"
    ret_str += "flux_tower_sites: " + self._flux_tower_sites + "\n"
    ret_str += "flux_tower_sites_to_exclude" + self._flux_tower_sites_to_exclude + "\n"
    ret_str += "last_used_nature_run" + self._last_used_nature_run + "\n"
    ret_str += "input_hdf5_files: " + self._input_hdf5_files + "\n"
    ret_str += "output_hdf5_files: " + self._output_hdf5_files
    return ret_str

  def reference_bplut_table(self):
    return self._reference_bplut_table

  def flux_tower_sites(self):
    return self._flux_tower_sites

  def flux_tower_sites_to_exclude(self):
    return self._flux_otwer_sites_to_exclude

  def last_used_nature_run(self):
    return self._last_used_nature_run

  def input_hdf5_files(self):
    return self._input_hdf5_files

  def output_hdf5_files(self):
    return self._output_hdf5_files

def main(argv):
  if len(argv) < 1:
    print ("usage: <config file>")
    exit(1)  
  file_path = argv[0]
  config_file = ConfigFile(file_path)
  print (config_file)

if __name__ == "__main__":
  main(sys.argv[1:])
