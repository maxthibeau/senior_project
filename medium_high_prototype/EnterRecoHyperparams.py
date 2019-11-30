from BasePage import *
from PyQt5.QtCore import Qt

class EnterRecoHyperparams(BasePage):

  def __init__(self, next_page_function, page_title):
    BasePage.__init__(self, next_page_function, page_title)
    page_label = QtWidgets.QLabel("Choose a Prh and Pk")
    second_page_label = QtWidgets.QLabel("(Between 0 and 1)")

    self.Prh_label = QtWidgets.QLabel("Prh:")
    self.Prh_textbox = QtWidgets.QLineEdit(self)
    self.Prh_textbox.textChanged.connect(self.updatePrhslide)
    self.Prh_slide = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    self.Prh_slide.setMinimum(0)
    self.Prh_slide.setMaximum(100)
    self.Prh_slide.setTickInterval(10)
    self.Prh_slide.setTickPosition(QtWidgets.QSlider.TicksBelow)
    self.Prh_slide.setSingleStep(10)
    self.Prh_slide.valueChanged.connect(self.valuePrhchange)
    Prh_layout = QtWidgets.QHBoxLayout()
    Prh_layout.addWidget(self.Prh_label)
    Prh_layout.addWidget(self.Prh_slide)
    Prh_layout.addWidget(self.Prh_textbox)

    self.Pk_label = QtWidgets.QLabel("Pk:")
    self.Pk_textbox = QtWidgets.QLineEdit(self)
    self.Pk_textbox.textChanged.connect(self.updatePkslide)
    self.Pk_slide = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    self.Pk_slide.setMinimum(0)
    self.Pk_slide.setMaximum(100)
    self.Pk_slide.setTickInterval(10)
    self.Pk_slide.setTickPosition(QtWidgets.QSlider.TicksBelow)
    self.Pk_slide.setSingleStep(10)
    self.Pk_slide.valueChanged.connect(self.valuePkchange)
    Pk_layout = QtWidgets.QHBoxLayout()
    Pk_layout.addWidget(self.Pk_label)
    Pk_layout.addWidget(self.Pk_slide)
    Pk_layout.addWidget(self.Pk_textbox)

    # move on to next page
    next_button = QtWidgets.QPushButton("Display RECO RAMP Functions")
    next_button.clicked.connect(self.next_page)

    main_layout = QtWidgets.QVBoxLayout(self)
    main_layout.addWidget(page_label)
    main_layout.addWidget(second_page_label)
    main_layout.addLayout(Prh_layout)
    main_layout.addLayout(Pk_layout)
    main_layout.addWidget(next_button)
    self.setLayout(main_layout)

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
      if not self.valid_value(float(value)):
        return False
      value=float(value)*100
      self.Prh_slide.setValue(value)
  def updatePkslide(self,value):
      if not self.valid_value(float(value)):
        return False
      value=float(value)*100
      self.Pk_slide.setValue(value)
  def next_page(self):
    Prh = self.Prh_textbox.text()
    Pk = self.Pk_textbox.text()
    if not self.valid_value(Prh):
      self.Prh_label.setText("Prh needs to be a float between 0 and 1")
      self.Prh_label.setStyleSheet("color: red;")

    if not self.valid_value(Pk):
      self.Pk_label.setText("Pk needs to be a float between 0 and 1")
      self.Pk_label.setStyleSheet("color: red;")

    if self.valid_value(Prh) and self.valid_value(Pk):
      self.next_window.emit()
      self.hide()
