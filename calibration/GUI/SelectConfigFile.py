from GUI.BasePage import *
# from GUI.TopBarLayout import *

class SelectConfigFile(BasePage):

  def __init__(self, width, height, page_title):
    BasePage.__init__(self, width, height)

    # config file browser
    # NOTE: make textbox for file name
    self.file_name = QtWidgets.QLabel("Select Configuration File")
    cfg_file_browser = QtWidgets.QPushButton("Browse")
    cfg_file_browser.clicked.connect(self.get_file)
    # layout of config file grabber
    cfg_file_browser_layout = QtWidgets.QHBoxLayout()
    cfg_file_browser_layout.addWidget(self.file_name)
    cfg_file_browser_layout.addWidget(cfg_file_browser)

    # next page
    next_btn = QtWidgets.QPushButton("Select PFT")
    next_btn.setToolTip('Select PFT')
    next_btn.clicked.connect(self.next_page)
    # previous page
    prev_btn = QtWidgets.QPushButton("Opening Screen")
    prev_btn.setToolTip("Opening Screen")
    prev_btn.clicked.connect(self.prev_page)
    # navigation
    navigation_layout = QtWidgets.QHBoxLayout()
    navigation_layout.addWidget(prev_btn)
    navigation_layout.addWidget(next_btn)

    # combine elements into layout
    main_layout = QtWidgets.QVBoxLayout()
    # main_layout.addLayout(TopBarLayout(width, height))
    main_layout.addLayout(cfg_file_browser_layout)
    main_layout.addLayout(navigation_layout)
    self.setLayout(main_layout)
    self.setWindowTitle(page_title)

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
    else:
      self.next_window.emit()
      self.hide()
