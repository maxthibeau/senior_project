from BasePage import *

class OpeningScreen(BasePage):

  def __init__(self, next_page_function, page_title):
    BasePage.__init__(self, next_page_function, page_title)

    # NTSG Logo
    ntsg_logo_label = QtWidgets.QLabel(self)
    img = QtGui.QPixmap('NTSG-logo.jpg')
    ntsg_logo_label.setPixmap(img)

    # Button to next page
    begin_calibration_button = QtWidgets.QPushButton("Begin Calibration")
    begin_calibration_button.setToolTip('Start the calibration process')
    begin_calibration_button.clicked.connect(self.next_page)

    # create layout
    main_layout = QtWidgets.QVBoxLayout()
    main_layout.addWidget(ntsg_logo_label)
    main_layout.addWidget(begin_calibration_button)
    self.setLayout(main_layout)
