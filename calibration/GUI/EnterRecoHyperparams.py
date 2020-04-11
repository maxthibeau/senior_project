from GUI.BasePage import *
from PyQt5.QtCore import Qt

class EnterRecoHyperparams(BasePage):

  def __init__(self, width, height, page_title):
    BasePage.__init__(self, width, height)
    page_label = QtWidgets.QLabel("9. Choose a Prh and Pk (Between 0 and 1)")
    page_label.setToolTip('Prh (Percentile of RH/Kmult to use in SOC pools) and Pk (Percentile to use as minimum threshold for acceptable Kmult values)')
    page_label.setFont(QtGui.QFont("SansSerif", 13))
    self.pft_label = QtWidgets.QLabel("Current PFT: "+self.pft_chooser(1)) #TODO: change to get correct pft ind
    self.pft_label.setFont(QtGui.QFont("SansSerif", 11))

    self.Prh_label = QtWidgets.QLabel("Prh:")
    self.Prh_label.setToolTip('Percentile of RH/Kmult to use in SOC pools')
    self.Prh_label.setFont(QtGui.QFont("SansSerif", 10))
    self.Prh_error_label = QtWidgets.QLabel("Error: Prh must be between 0 and 1")
    self.Prh_error_label.setFont(QtGui.QFont("SansSerif", 10))
    self.Prh_error_label.setVisible(False)
    self.Prh_textbox = QtWidgets.QLineEdit(self)
    self.Prh_textbox.textChanged.connect(self.updatePrhslide)
    self.Prh_slide = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    self.Prh_slide.setMinimum(0)
    self.Prh_slide.setMaximum(100)
    self.Prh_slide.setTickInterval(10)
    self.Prh_slide.setTickPosition(QtWidgets.QSlider.TicksBelow)
    self.Prh_slide.setSingleStep(10)
    self.Prh_slide.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    self.Prh_slide.valueChanged.connect(self.valuePrhchange)
    Prh_layout = QtWidgets.QGridLayout()
    Prh_layout.addWidget(self.Prh_label,1,0,1,0)
    Prh_layout.addWidget(self.Prh_slide,1,0,2,2)
    Prh_layout.addWidget(self.Prh_textbox,1,2,2,4)
    Prh_layout.addWidget(self.Prh_error_label,2,0,1,0)

    self.Pk_label = QtWidgets.QLabel("Pk:")
    self.Pk_label.setToolTip('Percentile to use as minimum threshold for acceptable Kmult values')
    self.Pk_label.setFont(QtGui.QFont("SansSerif", 10))
    self.Pk_error_label = QtWidgets.QLabel("Error: Pk must be between 0 and 1")
    self.Pk_error_label.setFont(QtGui.QFont("SansSerif", 10))
    self.Pk_error_label.setVisible(False)
    self.Pk_textbox = QtWidgets.QLineEdit(self)
    self.Pk_textbox.textChanged.connect(self.updatePkslide)
    self.Pk_slide = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    self.Pk_slide.setMinimum(0)
    self.Pk_slide.setMaximum(100)
    self.Pk_slide.setTickInterval(10)
    self.Pk_slide.setTickPosition(QtWidgets.QSlider.TicksBelow)
    self.Pk_slide.setSingleStep(10)
    self.Pk_slide.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    self.Pk_slide.valueChanged.connect(self.valuePkchange)
    Pk_layout = QtWidgets.QGridLayout()
    Pk_layout.addWidget(self.Pk_label,1,0,1,0)
    Pk_layout.addWidget(self.Pk_slide,1,0,2,2)
    Pk_layout.addWidget(self.Pk_textbox,1,2,2,4)
    Pk_layout.addWidget(self.Pk_error_label,2,0,1,0)
    
    # move on to next page
    button_layout = QtWidgets.QHBoxLayout()
    prev_button = QtWidgets.QPushButton("Redisplay GPP \nParameter Difference")
    prev_button.setFixedSize(250,75)
    prev_button.setFont(QtGui.QFont("SansSerif", 9, QtGui.QFont.Bold))
    prev_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    prev_button.clicked.connect(self.prev_page)
    next_button = QtWidgets.QPushButton("Proceed")
    next_button.setToolTip('Continue')
    next_button.setFont(QtGui.QFont("SansSerif", 9, QtGui.QFont.Bold))
    next_button.setFixedSize(250,75)
    next_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    next_button.clicked.connect(self.next_page)
    button_layout.addWidget(prev_button)
    button_layout.addWidget(next_button)

    main_layout = QtWidgets.QGridLayout()
    main_layout.addWidget(page_label,1,0,1,0,alignment=Qt.AlignHCenter)
    main_layout.addWidget(self.pft_label,1,0,2,0,alignment=Qt.AlignHCenter)
    main_layout.addLayout(Prh_layout,2,0,4,0)
    main_layout.addLayout(Pk_layout,5,0,4,0)
    main_layout.addLayout(button_layout,7,0,6,0)
    self.setLayout(main_layout)
    self.setWindowTitle(page_title)

  def valid_value(self, value):
    try:
      return 0.0 <= float(value) and float(value) <= 1.0
    except ValueError:
      return False

  def valuePrhchange(self,value):
      value=value/100.0
      self.Prh_textbox.setText(str(value))
  def valuePkchange(self,value):
      value=value/100.0
      self.Pk_textbox.setText(str(value))
  def updatePrhslide(self,value):
      if not self.valid_value(value):
        return False
      value=float(value)*100
      self.Prh_slide.setValue(value)
  def updatePkslide(self,value):
      if not self.valid_value(value):
        return False
      value=float(value)*100
      self.Pk_slide.setValue(value)

  def next_page(self):
    Prh = self.Prh_textbox.text()
    Pk = self.Pk_textbox.text()
    if not self.valid_value(Prh):
      self.Prh_error_label.setText("Prh needs to be a float between 0 and 1")
      self.Prh_error_label.setStyleSheet("color: red;")
      self.Prh_error_label.setVisible(True)

    if not self.valid_value(Pk):
      self.Pk_error_label.setText("Pk needs to be a float between 0 and 1")
      self.Pk_error_label.setStyleSheet("color: red;")
      self.Pk_error_label.setVisible(True)
      
    if(self.valid_value(Prh)):
      self.Prh_error_label.setVisible(False)
      
    if(self.valid_value(Pk)):
      self.Pk_error_label.setVisible(False)
      
    if self.valid_value(Prh) and self.valid_value(Pk):
      self.next_window.emit()
      self.hide()
