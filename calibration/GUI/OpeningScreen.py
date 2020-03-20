from GUI.BasePage import *

class OpeningScreen(BasePage):

  def __init__(self, width, height, page_title):
    BasePage.__init__(self, width, height)

    # NTSG Logo
    ntsg_logo_label = QtWidgets.QLabel(self)
    img = QtGui.QPixmap('GUI/images/cover_page.jpg')
    ntsg_logo_label.setPixmap(img)

    # Button to next page
    begin_calibration_button = QtWidgets.QPushButton("Begin Calibration")
    begin_calibration_button.setToolTip('Start the calibration process')
    begin_calibration_button.clicked.connect(self.next_page)
    begin_calibration_button.setFixedSize(400,100)
    begin_calibration_button.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

    # create layout
    img_layout = QtWidgets.QHBoxLayout()
    img_layout.addWidget(ntsg_logo_label)

    main_layout = QtWidgets.QVBoxLayout()
    main_layout.addLayout(img_layout)
    main_layout.addWidget(begin_calibration_button, alignment=Qt.AlignCenter)
    self.setLayout(main_layout)
    self.setWindowTitle(page_title)
