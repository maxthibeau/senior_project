from GUI.BasePage import *

class NumericalSpinups(BasePage):

   def __init__(self, width, height, page_title):
      BasePage.__init__(self, width, height)
      self.step_label = QtWidgets.QLabel("13. Numerical Spin-Up Iterations")
      self.step_label.setFont(QtGui.QFont("SansSerif", 13))
      self.pft_label = QtWidgets.QLabel("Current PFT: "+self.pft_chooser(1)) #TODO: change to get correct pft ind
      self.pft_label.setFont(QtGui.QFont("SansSerif", 11))
      self.page_label = QtWidgets.QLabel("Choose a Number of Numerical Iterations: ")
      self.page_label.setToolTip('About 10 should do')
      self.page_label.setFont(QtGui.QFont("SansSerif", 10))
      self.Num_textbox = QtWidgets.QSpinBox(self)
      box_layout = QtWidgets.QHBoxLayout()
      box_layout.addWidget(self.page_label)
      box_layout.addWidget(self.Num_textbox)

      # move on to next page
      next_button = QtWidgets.QPushButton("Simulate")
      next_button.setToolTip('Run the simulation')
      next_button.setFixedSize(250,75)
      next_button.setFont(QtGui.QFont("SansSerif", 9, QtGui.QFont.Bold))
      next_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      next_button.clicked.connect(self.next_page)
      prev_button = QtWidgets.QPushButton("Redisplay SOC estimation")
      prev_button.setFixedSize(250,75)
      prev_button.setFont(QtGui.QFont("SansSerif", 9, QtGui.QFont.Bold))
      prev_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      prev_button.clicked.connect(self.prev_page)
      button_layout = QtWidgets.QHBoxLayout()
      button_layout.addWidget(prev_button)
      button_layout.addWidget(next_button)

      main_layout = QtWidgets.QGridLayout(self)
      main_layout.addWidget(self.step_label,1,0,1,0,alignment=Qt.AlignHCenter)
      main_layout.addWidget(self.pft_label,1,0,2,0,alignment=Qt.AlignHCenter)
      main_layout.addLayout(box_layout,2,0,4,0)
      main_layout.addLayout(button_layout,4,0,5,0)
      self.setLayout(main_layout)
      self.setWindowTitle(page_title)
   def valid_value(self, value):
     try:
       return int(value) > 0
     except ValueError:
       return False

   def next_page(self):
      num = self.Num_textbox.text()
      if not self.valid_value(num):
        self.page_label.setText("Number needs to be a whole number above 0")
        self.page_label.setStyleSheet("color: red;")

      if self.valid_value(num):
        self.next_window.emit()
        self.hide()
