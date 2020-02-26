from GUI.BasePage import *

class NumericalSpinups(BasePage):

   def __init__(self, width, height, page_title):
      BasePage.__init__(self, width, height)
      self.page_label = QtWidgets.QLabel("Choose a Number of Numerical Iterations: ")
      self.page_label.setToolTip('About 10 should do')

      self.Num_textbox = QtWidgets.QSpinBox(self)

      # move on to next page
      next_button = QtWidgets.QPushButton("Simulate")
      next_button.setToolTip('Run the simulation')
      next_button.clicked.connect(self.next_page)
      prev_button = QtWidgets.QPushButton("Redisplay SOC esimation")
      prev_button.clicked.connect(self.prev_page)

      main_layout = QtWidgets.QVBoxLayout(self)
      main_layout.addWidget(self.page_label)
      main_layout.addWidget(self.Num_textbox)
      main_layout.addWidget(prev_button)
      main_layout.addWidget(next_button)
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
