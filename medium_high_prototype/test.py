from BasePage import *

class RecoHyperparameters(BasePage):

  def __init__(self, next_page_function, page_title):
    BasePage.__init__(self, next_page_function, page_title)

  page_label = QtWidgets.QLabel("Choose a Prh and Pk")
  second_page_label = QtWidgets.QLabel("Between 0 and 1")
  
  Prh_label = QtWidgets.QLabel("Prh:")  
  Prh_insert = QtWidgets.QLineEdit(self)
  Prh_layout = QtWidgets.QHBoxLayout()
  Prh_layout.addWidget(Prh_label)
  Prh_layout.addWidget(Q
  Pk_label = QtWidgets.QLabel("Pk:")
  Pk_insert = QtWidgets.QLineEdit(self)

  # move on to next page
  next_button = QtWidgets.QPushButton("Display RECO RAMP Functions")
  next_button.clicked.connect(self.next_page)
