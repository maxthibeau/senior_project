from BasePage import *

class SimulationStatistics(BasePage):

   def __init__(self, next_page_function, page_title, exit_option):
      BasePage.__init__(self, next_page_function, page_title)
      page_label = QtWidgets.QLabel("Simulation Completed")

      self.Rval_label = QtWidgets.QLabel("Pearson's R-Value: ")
      self.Rval_textbox = QtWidgets.QLineEdit(self)
      self.Rval_textbox.setReadOnly(True)
      rval = 0.02 #should add error check, real value will be passed in
      self.Rval_textbox.setText(str(rval))
      Rval_layout = QtWidgets.QHBoxLayout()
      Rval_layout.addWidget(self.Rval_label)
      Rval_layout.addWidget(self.Rval_textbox)

      self.RMSEgpp_label = QtWidgets.QLabel("GPP RMSE: ")
      self.RMSEgpp_label.setToolTip('Gross Primary Production Root Mean Squared Error')
      self.RMSEgpp_textbox = QtWidgets.QLineEdit(self)
      self.RMSEgpp_textbox.setReadOnly(True)
      RMSEgpp = 0.50 #should add error check for value handling, real value will be passed in
      self.RMSEgpp_textbox.setText(str(RMSEgpp))
      GPP_layout = QtWidgets.QHBoxLayout()
      GPP_layout.addWidget(self.RMSEgpp_label)
      GPP_layout.addWidget(self.RMSEgpp_textbox)

      self.RMSEreco_label = QtWidgets.QLabel("RECO RMSE: ")
      self.RMSEreco_label.setToolTip('Ecosystem Respiration Root Mean Squared Error')
      self.RMSEreco_textbox = QtWidgets.QLineEdit(self)
      self.RMSEreco_textbox.setReadOnly(True)
      RMSEreco = 0.25 #should add error check for value handling, real value will be passed in
      self.RMSEreco_textbox.setText(str(RMSEreco))
      RECO_layout = QtWidgets.QHBoxLayout()
      RECO_layout.addWidget(self.RMSEreco_label)
      RECO_layout.addWidget(self.RMSEreco_textbox)

      self.RMSEnee_label = QtWidgets.QLabel("NEE RMSE: ")
      self.RMSEnee_label.setToolTip('Net Ecosystem Exchange Root Mean Squared Error')
      self.RMSEnee_textbox = QtWidgets.QLineEdit(self)
      self.RMSEnee_textbox.setReadOnly(True)
      RMSEnee = 0.75 #should add error check for value handling, real value will be passed in
      self.RMSEnee_textbox.setText(str(RMSEnee))
      NEE_layout = QtWidgets.QHBoxLayout()
      NEE_layout.addWidget(self.RMSEnee_label)
      NEE_layout.addWidget(self.RMSEnee_textbox)

      #gives user option to continue to exit the program
      exit_button = QtWidgets.QPushButton("Exit")
      exit_button.setToolTip('Quits the Program')
      exit_button.clicked.connect(self.exit)
      # move on to next page
      next_button = QtWidgets.QPushButton("Select Next PFT")
      next_button.clicked.connect(self.next_page)
      button_layout = QtWidgets.QHBoxLayout()
      button_layout.addWidget(exit_button)
      button_layout.addWidget(next_button)

      main_layout = QtWidgets.QVBoxLayout(self)
      main_layout.addWidget(page_label)
      main_layout.addLayout(Rval_layout)
      main_layout.addLayout(GPP_layout)
      main_layout.addLayout(RECO_layout)
      main_layout.addLayout(NEE_layout)
      main_layout.addLayout(button_layout)
      self.setLayout(main_layout)

   def exit(self):
      self.hide()
      exit()
   def next_page(self):
      self.next_window.emit()
      self.hide()
