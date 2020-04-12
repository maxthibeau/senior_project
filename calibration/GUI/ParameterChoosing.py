from GUI.BasePage import *

class ParameterChoosing(BasePage):

  def __init__(self, width, height, page_title, params, tooltips, gpp_or_reco):
    BasePage.__init__(self, width, height)
    tooltip = tooltips
    self.params = params
    self.param_checkboxes = []

    if gpp_or_reco=="GPP":
       self.param_label = QtWidgets.QLabel("7. "+gpp_or_reco+" Optimization Parameters")
    else:
       self.param_label = QtWidgets.QLabel("11. "+gpp_or_reco+" Optimization Parameters")
    self.param_label.setFont(QtGui.QFont("SansSerif", 13, QtGui.QFont.Bold))
    #self.param_label.move(0,-100)
    self.pft_label = QtWidgets.QLabel("Current PFT: "+self.pft_chooser(1)) #TODO: change to get correct pft ind
    self.pft_label.setFont(QtGui.QFont("SansSerif", 11))
    
    self.top_layout = QtWidgets.QVBoxLayout()
    self.top_layout.addWidget(self.param_label,alignment=Qt.AlignCenter)
    self.top_layout.addWidget(self.pft_label,alignment=Qt.AlignHCenter | Qt.AlignBottom)
    self.top_layout.setAlignment(Qt.AlignCenter)

    for param in self.params:
      checkbox = QtWidgets.QCheckBox(param)
      checkbox.setFont(QtGui.QFont("SansSerif", 11))
      #Source: https://stackoverflow.com/questions/41784184/how-to-resize-qcheckbox
      checkbox.setStyleSheet("QCheckBox::indicator { width: 25px; height: 25px; }") #May have to change the check image to an image of a higher resolution
      if param in tooltip:
          checkbox.setToolTip(tooltip[param])
      self.param_checkboxes.append(checkbox)

    self.select_parameters_label = QtWidgets.QLabel("Select Parameters To Optimize")
    self.select_parameters_label.setFont(QtGui.QFont("SansSerif", 11,QtGui.QFont.Bold))
    self.select_parameters_label.setAlignment(Qt.AlignHCenter)
    #self.select_parameters_label.setStyleSheet("text-decoration: underline;")

    grid_layout = QtWidgets.QGridLayout()
    grid_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
    grid_layout.setHorizontalSpacing(20)
    for i in range(len(self.param_checkboxes)):
      param_checkbox = self.param_checkboxes[i]
      param_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
      num_checkboxes = len(self.param_checkboxes)
      param_checkbox.setChecked(True)
      if i < num_checkboxes / 2:
        grid_layout.addWidget(param_checkbox, i, 0)
      else:
        grid_layout.addWidget(param_checkbox, i - num_checkboxes / 2, 1)
    
    self.mid_layout = QtWidgets.QVBoxLayout()
    self.mid_layout.addWidget(self.select_parameters_label,alignment=Qt.AlignHCenter)
    self.mid_layout.addLayout(grid_layout)
    self.mid_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
    
    self.optimize_button = QtWidgets.QPushButton("Optimize Parameters")
    self.optimize_button.setFixedSize(250,75)
    self.optimize_button.setFont(QtGui.QFont("SansSerif", 9, QtGui.QFont.Bold))
    self.optimize_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    self.optimize_button.clicked.connect(self.next_page)
    
    self.prev_page_button = QtWidgets.QPushButton("Re-display old RAMP functions")
    self.prev_page_button.setFixedSize(250,75)
    self.prev_page_button.setFont(QtGui.QFont("SansSerif", 9, QtGui.QFont.Bold))
    self.prev_page_button.clicked.connect(self.prev_page)
    self.prev_page_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    button_layout = QtWidgets.QHBoxLayout()
    button_layout.addWidget(self.prev_page_button)
    button_layout.addWidget(self.optimize_button)

    main_layout = QtWidgets.QVBoxLayout()
    #main_layout.setSpacing(5)
    main_layout.addLayout(self.top_layout)
    main_layout.addLayout(self.mid_layout)
    main_layout.addLayout(button_layout)
    self.setLayout(main_layout)
    self.setWindowTitle(page_title)

  def parameters_selected(self):
    for param_checkbox in self.param_checkboxes:
      if param_checkbox.isChecked():
        return True
    return False

  def params_to_optimize(self):
    params_to_optimize = []
    for param_checkbox in self.param_checkboxes:
      if param_checkbox.isChecked():
        params_to_optimize.append(param_checkbox.text())
    return params_to_optimize

  def next_page(self):
    if not self.parameters_selected():
      self.select_parameters_label.setText("Select At least one Parameter:")
      self.select_parameters_label.setStyleSheet("color: red; text-decoration: underline;")
    else:
      BasePage.next_page(self)
