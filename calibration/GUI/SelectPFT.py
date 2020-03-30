from GUI.BasePage import *

class SelectPFT(BasePage):

  next_window = QtCore.pyqtSignal()
  prev_window = QtCore.pyqtSignal()

  def __init__(self, width, height, page_title, tooltips):
    BasePage.__init__(self, width, height)
    tooltip = tooltips

    title = QtWidgets.QLabel("2. Plant Functional Type (PFT) Selection Page")
    title.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
    # these widgets select a pft
    self.pft_selector_label = QtWidgets.QLabel("Select PFT (Hover over a PFT for additional information)")
    self.pft_selector_label.setToolTip("Select "+tooltip["PFT"])
    self.pft_selector_label.setFont(QtGui.QFont("Times", 12))
    self.pft_selector = QtWidgets.QComboBox()
    self.pft_selector.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    self.pft_selector.setFixedSize(350,75)
    self.pft_selector.setFont(QtGui.QFont("Times",12))
    self.pft_selector.addItem("Choose a PFT Here")
    self.pft_selector.setItemData(0,"Please select a pft from the list below",QtCore.Qt.ToolTipRole)
    self.pft_selector.addItem("Evergreen Needleleaf")
    self.pft_selector.setItemData(1,"ENF: "+tooltip["ENF"],QtCore.Qt.ToolTipRole)
    self.pft_selector.addItem("Evergreen Broadleaf")
    self.pft_selector.setItemData(2,"EBF: "+tooltip["EBF"],QtCore.Qt.ToolTipRole)
    self.pft_selector.addItem("Deciduous Needleleaf")
    self.pft_selector.setItemData(3,"DNF: "+tooltip["DNF"],QtCore.Qt.ToolTipRole)
    self.pft_selector.addItem("Deciduous Broadleaf")
    self.pft_selector.setItemData(4,"DBF: "+tooltip["DBF"],QtCore.Qt.ToolTipRole)
    self.pft_selector.addItem("Shrub")
    self.pft_selector.setItemData(5,"SHR: "+tooltip["SHR"],QtCore.Qt.ToolTipRole)
    self.pft_selector.addItem("Grass")
    self.pft_selector.setItemData(6,"GRS: "+tooltip["GRS"],QtCore.Qt.ToolTipRole)
    self.pft_selector.addItem("Cereal Crop")
    self.pft_selector.setItemData(7,"CCP: "+tooltip["CCP"],QtCore.Qt.ToolTipRole)
    self.pft_selector.addItem("Broadleaf Crop")
    self.pft_selector.setItemData(8,"BCP: "+tooltip["BCP"],QtCore.Qt.ToolTipRole)

    self.error_message = QtWidgets.QLabel("Please choose a PFT before proceeding")
    self.error_message.setStyleSheet("color: red;")
    self.error_message.setFont(QtGui.QFont("Times", 9))
    self.error_message.setVisible(False)
    # combine pft selection widgets into a layout
    top_layout = QtWidgets.QHBoxLayout()
    top_layout.setAlignment(Qt.AlignCenter)
    top_layout.addWidget(self.pft_selector_label)
    top_layout.addWidget(self.pft_selector)

    # give user navigation abilities
    next_page = QtWidgets.QPushButton("Proceed")
    next_page.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    next_page.setFont(QtGui.QFont("Times", 9, QtGui.QFont.Bold))
    next_page.setFixedSize(250,75)
    # next_page.setToolTip('Continue')
    next_page.clicked.connect(self.next_check)

    prev_page = QtWidgets.QPushButton("Choose a different config file")
    prev_page.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    prev_page.setFont(QtGui.QFont("Times", 9, QtGui.QFont.Bold))
    prev_page.setFixedSize(250,75)
    prev_page.clicked.connect(self.prev_page)

    # combine navigation buttons into one layout
    bottom_layout = QtWidgets.QHBoxLayout()
    bottom_layout.addWidget(prev_page)
    bottom_layout.addWidget(next_page)
    bottom_layout.setAlignment(Qt.AlignCenter)

    # combine pft selection and navigation elements into one
    main_layout = QtWidgets.QVBoxLayout()
    main_layout.addWidget(title, alignment=Qt.AlignHCenter)
    main_layout.addLayout(top_layout)
    main_layout.addWidget(self.error_message,alignment=Qt.AlignHCenter)
    main_layout.addLayout(bottom_layout)
    self.setLayout(main_layout)
    self.setWindowTitle(page_title)

  def next_check(self):
    if(self.pft_selector.currentIndex() == 0):
      self.error_message.setVisible(True)
    else:
      self.error_message.setVisible(False)
      self.next_page(self.pft_selector.currentIndex()-1) #subtract 1 since first option is not a PFT
