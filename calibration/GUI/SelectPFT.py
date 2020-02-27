from GUI.BasePage import *

class SelectPFT(BasePage):

  next_window = QtCore.pyqtSignal()
  prev_window = QtCore.pyqtSignal()

  def __init__(self, width, height, page_title):
    BasePage.__init__(self, width, height)

    # these widgets select a pft
    self.pft_selector_label = QtWidgets.QLabel("Select PFT")
    self.pft_selector_label.setToolTip('Select Plant Function Type')
    self.pft_selector = QtWidgets.QComboBox()
    self.pft_selector.addItem("Evergreen Needleleaf")
    self.pft_selector.addItem("Evergreen Broadleaf")
    self.pft_selector.addItem("Deciduous Needleleaf")
    self.pft_selector.addItem("Deciduous Broadleaf")
    self.pft_selector.addItem("Shrub") 
    self.pft_selector.addItem("Grass")
    self.pft_selector.addItem("Cereal Crop")
    self.pft_selector.addItem("Broadleaf Crop")

    # combine pft selection widgets into a layout
    top_layout = QtWidgets.QHBoxLayout()
    top_layout.addWidget(self.pft_selector_label)
    top_layout.addWidget(self.pft_selector)
    
    # give user navigation abilities
    next_page = QtWidgets.QPushButton("Smooth GPP Outliers")
    # next_page.setToolTip('Continue')
    next_page.clicked.connect(self.next_page)

    prev_page = QtWidgets.QPushButton("Re-select config file")
    prev_page.clicked.connect(self.prev_page)

    # combine navigation buttons into one layout
    bottom_layout = QtWidgets.QHBoxLayout()
    bottom_layout.addWidget(prev_page)
    bottom_layout.addWidget(next_page)

    # combine pft selection and navigation elements into one
    main_layout = QtWidgets.QVBoxLayout()
    main_layout.addLayout(top_layout)
    main_layout.addLayout(bottom_layout)
    self.setLayout(main_layout)     
    self.setWindowTitle(page_title)
