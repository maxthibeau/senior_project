from BasePage import *

class SelectConfigFile(BasePage):

  def __init__(self, next_page_function, page_title):
    BasePage.__init__(self, next_page_function, page_title)

    # layout for displaying and selectin config file
    self.file_name = QtWidgets.QLabel("Select Configuration File")
    get_config_file_button = QtWidgets.QPushButton("Browse")
    get_config_file_button.clicked.connect(self.get_file)
 
    # layout of config file grabbing
    top_layout = QtWidgets.QHBoxLayout()    
    top_layout.addWidget(self.file_name)
    top_layout.addWidget(get_config_file_button)

    # move on to next page
    next_button = QtWidgets.QPushButton("Select PFT")
    next_button.clicked.connect(self.next_page)

    # combine elements into layout
    main_layout = QtWidgets.QVBoxLayout()
    main_layout.addLayout(top_layout)
    main_layout.addWidget(next_button)
    self.setLayout(main_layout)

  def get_file(self):
    filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose Config File', '.', '*.cfg files')
    if filename != '':
      self.file_name.setText(filename)
      self.file_name.setStyleSheet("color: black;")

  def next_page(self):
    if self.file_name.text() == 'Select Configuration File' or self.file_name.text() == 'Please select a valid config file':
      self.file_name.setStyleSheet("color: red;")
      self.file_name.setText("Please select a valid config file")
    else:
      self.next_window.emit()
      self.hide()
