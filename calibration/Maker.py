from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import * #QApplication, QWidget, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import * # QIcon
import sys
import os

###########################################################################################
# GUI FOR CONFIG FILE MAKER (CLI file maker seems pointless) ##############################
###########################################################################################

class Maker(QWidget):

  def __init__(self):
    super().__init__()
    self.title = 'Config File Creation Wizard'
    self.left = 300
    self.top = 200
    self.width = 800
    self.height = 60
    self.initUI()
        
  def initUI(self):
    # Widgets ###################
    mandatory_label = QLabel("These Fields are Required")

    reference_bplut_table_label = QLabel("Reference BPlut Table:")
    reference_bplut_table_button = QPushButton("Select File")
    reference_bplut_table_button.clicked.connect(self.reference_bplut_table_get_file)
    self.reference_bplut_table_edit = QLineEdit()

    flux_tower_sites_label = QLabel("Included Flux Tower Sites:")
    flux_tower_sites_button = QPushButton("Select File")
    flux_tower_sites_button.clicked.connect(self.flux_tower_sites_get_file)
    self.flux_tower_sites_edit = QLineEdit()

    flux_tower_sites_to_exclude_label = QLabel("Excluded Flux Tower Sites")
    flux_tower_sites_to_exclude_button = QPushButton("Select File")
    flux_tower_sites_to_exclude_button.clicked.connect(self.flux_tower_sites_to_exclude_get_file)
    self.flux_tower_sites_to_exclude_edit = QLineEdit()

    last_used_nature_run_label = QLabel("Last Used Nature Run")
    last_used_nature_run_button = QPushButton("Select File")
    last_used_nature_run_button.clicked.connect(self.last_used_nature_run_get_file)
    self.last_used_nature_run_edit = QLineEdit()

    input_hdf5_files_label = QLabel("Input HDF5 Files")
    input_hdf5_files_button = QPushButton("Select Files")
    input_hdf5_files_button.clicked.connect(self.input_hdf5_files_get_files)
    self.input_hdf5_files_edit = QLineEdit()

    output_hdf5_files_label = QLabel("Output HDF5 Files")
    output_hdf5_files_button = QPushButton("Select Files")
    output_hdf5_files_button.clicked.connect(self.output_hdf5_files_get_files)
    self.output_hdf5_files_edit = QLineEdit()



    submit_label = QLabel("Enter Filename (e.g. config.cfg):")
    self.submit_edit = QLineEdit()
    submit_button = QPushButton("Create Config File")
    submit_button.clicked.connect(self.submit_and_save)

    # Layout ####################

    grid = QGridLayout()
    #grid.setSpacing(7)
      
    grid.addWidget(mandatory_label,1,3,1,3)

    grid.addWidget(reference_bplut_table_label,2,1,1,2)
    grid.addWidget(reference_bplut_table_button,2,3,1,1)
    grid.addWidget(self.reference_bplut_table_edit,2,4,1,4)

    grid.addWidget(flux_tower_sites_label,3,1,1,2)
    grid.addWidget(flux_tower_sites_button,3,3,1,1)
    grid.addWidget(self.flux_tower_sites_edit,3,4,1,4)

    grid.addWidget(flux_tower_sites_to_exclude_label,4,1,1,2)
    grid.addWidget(flux_tower_sites_to_exclude_button,4,3,1,1)
    grid.addWidget(self.flux_tower_sites_to_exclude_edit,4,4,1,4)

    grid.addWidget(last_used_nature_run_label,5,1,1,2)
    grid.addWidget(last_used_nature_run_button,5,3,1,1)
    grid.addWidget(self.last_used_nature_run_edit,5,4,1,4)

    grid.addWidget(input_hdf5_files_label,6,1,1,2)
    grid.addWidget(input_hdf5_files_button,6,3,1,1)
    grid.addWidget(self.input_hdf5_files_edit,6,4,1,4)

    grid.addWidget(output_hdf5_files_label,7,1,1,2)
    grid.addWidget(output_hdf5_files_button,7,3,1,1)
    grid.addWidget(self.output_hdf5_files_edit,7,4,1,4)

    grid.addWidget(submit_label,8,1,1,2)
    grid.addWidget(self.submit_edit,8,3,1,4)
    grid.addWidget(submit_button,8,7,1,1)


    #grid.addWidget(,,,,)
      
      
      
      
    self.setLayout(grid)
    self.setGeometry(self.left, self.top, self.width, self.height)
    self.setWindowTitle(self.title)
    self.show()


  def reference_bplut_table_get_file(self):
    filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose File', '.', '*.csv, *.* files')
    if filename != '':
      self.reference_bplut_table_edit.setText(filename)

  def flux_tower_sites_get_file(self):
    filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose File', '.', '*.txt, *.* files')
    if filename != '':
      self.flux_tower_sites_edit.setText(filename)

  def flux_tower_sites_to_exclude_get_file(self):
    filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose File', '.', '*.txt, *.* files')
    if filename != '':
      self.flux_tower_sites_to_exclude_edit.setText(filename)

  def last_used_nature_run_get_file(self):
    filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose File', '.', '*.txt, *.* files')
    if filename != '':
      self.last_used_nature_run_edit.setText(filename)

  def input_hdf5_files_get_files(self):
    filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(self, 'Choose File', '.', '*.HDF5, *.* files')
    if filenames != '':
      self.input_hdf5_files_edit.setText(str(filenames).replace("'","").replace("[","").replace("]",""))

  def output_hdf5_files_get_files(self):
    filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(self, 'Choose File', '.', '*.HDF5, *.* files')
    if filenames != '':
      self.output_hdf5_files_edit.setText(str(filenames).replace("'","").replace("[","").replace("]",""))

  def submit_and_save(self):
    er = False
    if self.submit_edit.text() == "":
      er = True
      err("")
    if self.reference_bplut_table_edit.text() == "":
      er = True
      err("")
    if self.flux_tower_sites_edit.text() == "":
      er = True
      err("")
    if self.flux_tower_sites_to_exclude_edit.text() == "":
      er = True
      err("")
    if self.last_used_nature_run_edit.text() == "":
      er = True
      err("")
    if self.input_hdf5_files_edit.text() == "":
      er = True
      err("")
    if self.output_hdf5_files_edit.text() == "":
      er = True
      err("")
    print(er)
    if not er:
      out = ""
      out += self.reference_bplut_table_edit.text() + "\n"
      out += self.flux_tower_sites_edit.text() + "\n"
      out += self.flux_tower_sites_to_exclude_edit.text() + "\n"
      out += self.last_used_nature_run_edit.text() + "\n"
      out += self.input_hdf5_files_edit.text() + "\n"
      out += self.output_hdf5_files_edit.text() #+ "\n"

      filename = self.submit_edit.text()
      out_file = open(filename, 'w')
      out_file.write(out)
      out_file.close()
    

def err(err_message):
  return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Maker()
    sys.exit(app.exec_())

'''
    optional_label = QLabel("These Fields are Optional")

    pfts_label = QLabel("Select Plant Function Types")
    self.pft_selector = QtWidgets.QComboBox()
    self.pft_selector.addItem("Evergreen Needleleaf")
    self.pft_selector.addItem("Evergreen Broadleaf")
    self.pft_selector.addItem("Deciduous Needleleaf")
    self.pft_selector.addItem("Deciduous Broadleaf")
    self.pft_selector.addItem("Shrub") 
    self.pft_selector.addItem("Grass")
    self.pft_selector.addItem("Cereal Crop")
    self.pft_selector.addItem("Broadleaf Crop")

    opt_params_label = QLabel("Select Parameters to Optimize")
'''

