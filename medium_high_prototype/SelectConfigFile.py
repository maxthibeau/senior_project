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

    # layout for output config file
    self.output_name = QtWidgets.QLabel("Output Config File Name")
    self.output_textbox = QtWidgets.QLineEdit(self)
    self.output_textbox.setPlaceholderText("[PFT name][date].HDF5")
    self.output_textbox.textChanged.connect(self.outputcheck)
    output_layout = QtWidgets.QHBoxLayout()
    output_layout.addWidget(self.output_name)
    output_layout.addWidget(self.output_textbox)

    # move on to next page
    next_button = QtWidgets.QPushButton("Select PFT")
    next_button.clicked.connect(self.next_page)

    # combine elements into layout
    main_layout = QtWidgets.QVBoxLayout()
    main_layout.addLayout(top_layout)
    main_layout.addLayout(output_layout)
    main_layout.addWidget(next_button)
    self.setLayout(main_layout)

  def get_file(self):
    filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose Config File', '.', '*.cfg files')
    if filename != '':
      self.file_name.setText(filename)
      self.file_name.setStyleSheet("color: black;")

  def outputcheck(self,text):
     if not self.valid_name(text):
         self.output_label.setText("Please enter a valid output file name")
         self.output_label.setStyleSheet("color: red;")

  def valid_name(self,text):
      try:
        return text != ''
      except ValueError:
        return False

  def next_page(self):
    if self.file_name.text() == 'Select Configuration File' or self.file_name.text() == 'Please select a valid config file':
      self.file_name.setStyleSheet("color: red;")
      self.file_name.setText("Please select a valid config file")
    elif not self.valid_name(self.output_textbox.text):
      self.output_name.setStyleSheet("color: red;")
      self.output_name.setText("Please enter a valid output file name")
    else:
      self.next_window.emit()
      self.hide()
