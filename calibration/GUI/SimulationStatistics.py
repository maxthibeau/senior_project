from GUI.BasePage import *

class SimulationStatistics(BasePage):

   def __init__(self, width, height, page_title):
      BasePage.__init__(self, width, height)
      page_label = QtWidgets.QLabel("14. Simulation Completed")
      page_label.setFont(QtGui.QFont("SansSerif", 13, QtGui.QFont.Bold))
      self.pft = ""
      self.pft_label = QtWidgets.QLabel("Current PFT: "+self.pft_chooser(1)) #TODO: change to get correct pft ind
      self.pft_label.setFont(QtGui.QFont("SansSerif", 11))

      info_label = QtWidgets.QLabel("Simulation Statistics:")
      info_label.setFont(QtGui.QFont("SansSerif", 11, QtGui.QFont.Bold))

      self.Rval_label = QtWidgets.QLabel("Pearson's R-Value: ")
      self.Rval_label.setFont(QtGui.QFont("SansSerif", 11))
      self.Rval_textbox = QtWidgets.QLineEdit(self)
      self.Rval_textbox.setAlignment(Qt.AlignCenter)
      self.Rval_textbox.setFixedSize(200,50)
      self.Rval_textbox.setFont(QtGui.QFont("SansSerif", 11))
      self.Rval_textbox.setReadOnly(True)
      rval = 0.02 #should add error check, real value will be passed in
      self.Rval_textbox.setText(str(rval))
      Rval_layout = QtWidgets.QHBoxLayout()
      Rval_layout.addWidget(self.Rval_label,alignment=Qt.AlignHCenter)
      Rval_layout.addWidget(self.Rval_textbox,alignment=Qt.AlignHCenter)
      Rval_layout.setAlignment(Qt.AlignCenter)

      self.RMSEgpp_label = QtWidgets.QLabel("GPP RMSE: ")
      self.RMSEgpp_label.setToolTip('Gross Primary Production Root Mean Squared Error')
      self.RMSEgpp_label.setFont(QtGui.QFont("SansSerif", 11))
      self.RMSEgpp_textbox = QtWidgets.QLineEdit(self)
      self.RMSEgpp_textbox.setAlignment(Qt.AlignCenter)
      self.RMSEgpp_textbox.setFixedSize(200,50)
      self.RMSEgpp_textbox.setFont(QtGui.QFont("SansSerif", 11))
      self.RMSEgpp_textbox.setReadOnly(True)
      RMSEgpp = 0.50 #should add error check for value handling, real value will be passed in
      self.RMSEgpp_textbox.setText(str(RMSEgpp))
      GPP_layout = QtWidgets.QHBoxLayout()
      GPP_layout.addWidget(self.RMSEgpp_label,alignment=Qt.AlignHCenter)
      GPP_layout.addWidget(self.RMSEgpp_textbox,alignment=Qt.AlignHCenter)
      GPP_layout.setAlignment(Qt.AlignCenter)

      self.RMSEreco_label = QtWidgets.QLabel("RECO RMSE: ")
      self.RMSEreco_label.setFont(QtGui.QFont("SansSerif", 11))
      self.RMSEreco_label.setToolTip('Ecosystem Respiration Root Mean Squared Error')
      self.RMSEreco_textbox = QtWidgets.QLineEdit(self)
      self.RMSEreco_textbox.setAlignment(Qt.AlignCenter)
      self.RMSEreco_textbox.setFont(QtGui.QFont("SansSerif", 11))
      self.RMSEreco_textbox.setFixedSize(200,50)
      self.RMSEreco_textbox.setReadOnly(True)
      RMSEreco = 0.25 #should add error check for value handling, real value will be passed in
      self.RMSEreco_textbox.setText(str(RMSEreco))
      RECO_layout = QtWidgets.QHBoxLayout()
      RECO_layout.addWidget(self.RMSEreco_label,alignment=Qt.AlignHCenter)
      RECO_layout.addWidget(self.RMSEreco_textbox,alignment=Qt.AlignHCenter)
      RECO_layout.setAlignment(Qt.AlignCenter)

      self.RMSEnee_label = QtWidgets.QLabel("NEE RMSE: ")
      self.RMSEnee_label.setFont(QtGui.QFont("SansSerif", 11))
      self.RMSEnee_label.setToolTip('Net Ecosystem Exchange Root Mean Squared Error')
      self.RMSEnee_textbox = QtWidgets.QLineEdit(self)
      self.RMSEnee_textbox.setFont(QtGui.QFont("SansSerif", 11))
      self.RMSEnee_textbox.setAlignment(Qt.AlignCenter)
      self.RMSEnee_textbox.setFixedSize(200,50)
      self.RMSEnee_textbox.setReadOnly(True)
      RMSEnee = 0.75 #should add error check for value handling, real value will be passed in
      self.RMSEnee_textbox.setText(str(RMSEnee))
      NEE_layout = QtWidgets.QHBoxLayout()
      NEE_layout.addWidget(self.RMSEnee_label,alignment=Qt.AlignHCenter)
      NEE_layout.addWidget(self.RMSEnee_textbox,alignment=Qt.AlignHCenter)
      NEE_layout.setAlignment(Qt.AlignCenter)

      #gives user option to continue to exit the program
      exit_button = QtWidgets.QPushButton("Exit")
      exit_button.setToolTip('Quits the Program')
      exit_button.setFixedSize(250,75)
      exit_button.setFont(QtGui.QFont("SansSerif", 9, QtGui.QFont.Bold))
      exit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      exit_button.clicked.connect(self.exit)
      # move on to next page
      next_button = QtWidgets.QPushButton("Select Next PFT")
      next_button.setFixedSize(250,75)
      next_button.setFont(QtGui.QFont("SansSerif", 9, QtGui.QFont.Bold))
      next_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      next_button.clicked.connect(self.next_page)
      button_layout = QtWidgets.QHBoxLayout()
      button_layout.addWidget(exit_button)
      button_layout.addWidget(next_button)

      main_layout = QtWidgets.QVBoxLayout(self)
      main_layout.addWidget(page_label,alignment=Qt.AlignHCenter)
      main_layout.addWidget(self.pft_label,alignment=Qt.AlignHCenter)
      main_layout.addWidget(info_label,alignment=Qt.AlignHCenter)
      main_layout.addLayout(Rval_layout)
      main_layout.addLayout(GPP_layout)
      main_layout.addLayout(RECO_layout)
      main_layout.addLayout(NEE_layout)
      main_layout.addLayout(button_layout)
      self.setLayout(main_layout)
      self.setWindowTitle(page_title)

   def exit(self):
      self.hide()
      exit()
   def next_page(self):
      self.next_window.connect(self.next_page_ob.show)
      self.next_window.emit()
      self.hide()
   
   def set_pft(self,pft):
    self.pft = pft
    self.pft_label.setText("Current PFT: "+self.pft)
