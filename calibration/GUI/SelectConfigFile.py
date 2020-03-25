from GUI.BasePage import *
# from GUI.TopBarLayout import *

class SelectConfigFile(BasePage):

  def __init__(self, width, height, page_title):
    BasePage.__init__(self, width, height)

    # config file browser
    # NOTE: make textbox for file name
    title = QtWidgets.QLabel("1. Configuration File Selection")
    title.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
    self.file_name = QtWidgets.QLabel("Please select a Configuration File: ")
    self.file_name.setFont(QtGui.QFont("Times", 13))
    self.file_box = QtWidgets.QLineEdit("Choose a file (.cfg)")
    self.file_box.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Light))
    self.file_box.setReadOnly(True)
    self.file_box.setFixedSize(400,50)

    cfg_file_browser = QtWidgets.QPushButton("Browse Files")
    cfg_file_browser.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    cfg_file_browser.setFixedSize(200,50)
    cfg_file_browser.clicked.connect(self.get_file)

    cfg_button_field = QtWidgets.QFormLayout()
    cfg_button_field.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
    cfg_button_field.addRow(self.file_box,cfg_file_browser)
    cfg_button_field.setFormAlignment(Qt.AlignHCenter)

    # layout of config file grabber
    cfg_file_browser_layout = QtWidgets.QFormLayout()
    cfg_file_browser_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
    cfg_file_browser_layout.addRow(self.file_name,cfg_button_field)
    cfg_file_browser_layout.setFormAlignment(Qt.AlignCenter)

    # next page
    next_btn = QtWidgets.QPushButton("Continue to PFT Selection Page")
    next_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    next_btn.setToolTip('Select PFT')
    next_btn.clicked.connect(self.next_page)
    next_btn.setFont(QtGui.QFont("Times", 9, QtGui.QFont.Bold))
    next_btn.setFixedSize(250,75)
    # previous page
    #prev_btn = QtWidgets.QPushButton("Opening Screen")
    #prev_btn.setToolTip("Opening Screen")
    #prev_btn.clicked.connect(self.prev_page)
    # navigation
    navigation_layout = QtWidgets.QHBoxLayout()
    #navigation_layout.addWidget(prev_btn)
    navigation_layout.addWidget(next_btn)
    navigation_layout.setAlignment(Qt.AlignCenter)

    # combine elements into layout
    main_layout = QtWidgets.QVBoxLayout()
    # main_layout.addLayout(TopBarLayout(width, height))
    main_layout.addWidget(title,alignment=Qt.AlignHCenter)
    main_layout.addLayout(cfg_file_browser_layout)
    main_layout.addLayout(navigation_layout)
    self.setLayout(main_layout)
    self.setWindowTitle(page_title)

  def get_file(self):
    filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose Config File', '.', '*.cfg files')
    if filename != '':
      self.file_box.setText(filename)
      self.file_box.setStyleSheet("color: black;")

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
    if self.file_box.text() == 'Choose a file (.cfg)' or self.file_box.text() == 'Please select a valid config file':
      self.file_box.setStyleSheet("color: red;")
      self.file_box.setText("Please select a valid config file")
    else:
      self.next_window.emit()
      self.hide()
