import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

class ConfigFile():

  def __init__(self, file_path):
    with open(file_path) as f:
      lines = [x.strip() for x in f.readlines() if not x.startswith("#")]
      self._reference_bplut_table, self._flux_tower_sites, self._flux_tower_sites_to_exclude, self._last_used_nature_run, self._input_hdf5_files, self._output_hdf5_files = [x.strip() for x in lines[:6]] 
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

  def __str__(self):
    print (self._input_hdf5_files)
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

  def pfts(self):
    return self._pfts

  def optimization_parameters(self):
    return self._opt_params



###########################################################################################
# GUI FOR CONFIG FILE MAKER (CLI file maker seems pointless) ##############################
###########################################################################################

class Maker(QWidget):

    def __init__(self):
      super().__init__()
      self.title = 'Config File Creation Wizard'
      self.left = 100
      self.top = 100
      self.width = 800
      self.height = 600
      self.initUI()
        
    def initUI(self):
      # Widgets ###################
      mandatory_label = QLabel("These Fields are Required")

      reference_bplut_table_label = QLabel("Reference BPlut Table:")
      reference_bplut_table_button = QPushButton("Select File")
      reference_bplut_table_button.clicked.connect(self.reference_bplut_table_get_file())
      reference_bplut_table_edit = QLineEdit()

      flux_tower_sites_label = QLabel("Included Flux Tower Sites:")
      flux_tower_sites_button = QPushButton("Select File")
      flux_tower_sites_button.clicked.connect(self.flux_tower_sites_get_file())
      flux_tower_sites_edit = QLineEdit()

      flux_tower_sites_to_exclude_label = QLabel("Excluded Flux Tower Sites")
      flux_tower_sites_to_exclude_button = QPushButton("Select File")
      flux_tower_sites_to_exclude_button.clicked.connect(self.flux_tower_sites_to_exclude_get_file())
      flux_tower_sites_to_exclude_edit = QLineEdit()

      last_used_nature_run_label = QLabel("Last Used Nature Run")
      last_used_nature_run_button = QPushButton("Select File")
      last_used_nature_run_button_button.clicked.connect(self.last_used_nature_run_button_get_file())
      last_used_nature_run_edit = QLineEdit()

      input_hdf5_files_label = QLabel("Input HDF5 Files")
      input_hdf5_files_button = QPushButton("Select Files")
      input_hdf5_files_button.clicked.connect(self.input_hdf5_files_get_files())
      input_hdf5_files_edit = QLineEdit()

      output_hdf5_files_label = QLabel("Output HDF5 Files")
      output_hdf5_files_button = QPushButton("Select Files")
      output_hdf5_files_button.clicked.connect(self.output_hdf5_files_get_files())
      output_hdf5_files_edit = QLineEdit()


      optional_label = QLabel("These Fields are Optional")
      pfts_label = QLabel("Select Plant Function Types")
      opt_params_label = QLabel("Select Parameters to Optimize")


      #############################

      self.setWindowTitle(self.title)
      grid = QGridLayout()
      grid.setSpacing(7)
      
      
      
      
      
      
      
      self.setGeometry(self.left, self.top, self.width, self.height)
      self.show()


    def reference_bplut_table_get_file(self):
      filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose File', '.', '*.csv files')
        if filename != '':
        self.reference_bplut_table_edit.setText(filename)

    def flux_tower_sites_get_file(self):
      filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose File', '.', '*.txt files')
        if filename != '':
        self._edit.setText(filename)

    def flux_tower_sites_to_exclude_get_file(self):
      filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose File', '.', '*.txt files')
        if filename != '':
        self._edit.setText(filename)

    def last_used_nature_run_get_file(self):
      filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose File', '.', '*.txt files')
        if filename != '':
        self._edit.setText(filename)

    def input_hdf5_files_get_files(self):
      filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose File', '.', '*.HDF5 files')
        if filename != '':
        self._edit.setText(filename)

    def output_hdf5_files_get_file(self):
      filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose File', '.', '*.HDF5 files')
        if filename != '':
        self._edit.setText(filename)


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
