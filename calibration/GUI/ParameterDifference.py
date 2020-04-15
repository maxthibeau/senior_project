from GUI.BasePage import *

class ParameterDifference(BasePage):

  def __init__(self, width, height, page_title, optimized_params, gpp_or_reco, ramp_page):
    BasePage.__init__(self, width, height)
    
    self.pft = ""
    self.optimized_params = optimized_params
    self._ramp_page = ramp_page
    self.param_to_data = {}
    self.current_param_plotted_index = 0
    self.params = []
    for param in optimized_params:
      self.params.append(param)
      self.param_to_data[param] = [random.random(), random.random()]
    
    self.gpp_or_reco = gpp_or_reco
    assert gpp_or_reco in ("GPP", "RECO")
    
    self.current_param = self.params[self.current_param_plotted_index]
    
    #Remove later:
    #self.figure = plt.figure()
    #self.canvas = FigureCanvas(self.figure)
    #self.toolbar = NavigationToolbar(self.canvas, self)
    #self.plot_chosen_ramp_function()
    
    #Table Settings
    self.comp_table = QtWidgets.QTableWidget(2,3)
    self.comp_table.setFixedSize(400,125)
    self.row_header = self.comp_table.verticalHeader()
    self.row_header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
    self.comp_table.setItem(0,1,QtWidgets.QTableWidgetItem("Original"))
    self.comp_table.setItem(0,2,QtWidgets.QTableWidgetItem("Updated Fit"))
    self.comp_table.setItem(1,0,QtWidgets.QTableWidgetItem(self.gpp_or_reco + " vs " + self.current_param))
    self.comp_table.setItem(1,1,QtWidgets.QTableWidgetItem(str(self.param_to_data[self.current_param][0])))
    self.comp_table.setItem(1,2,QtWidgets.QTableWidgetItem(str(self.param_to_data[self.current_param][1])))
    
    #Next Button Settings
    next_param_button = QtWidgets.QPushButton(">")
    next_param_button.setFixedSize(50,275)
    next_param_button.setToolTip('Go to next optimized ramp function')
    next_param_button.setFont(QtGui.QFont("SansSerif", 12, QtGui.QFont.Bold))
    next_param_button.clicked.connect(self.next_table)
    next_param_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    prev_param_button = QtWidgets.QPushButton("<")
    prev_param_button.setFont(QtGui.QFont("SansSerif", 12, QtGui.QFont.Bold))
    prev_param_button.setFixedSize(50,275)
    prev_param_button.setToolTip('Go to previous optimized ramp function')
    prev_param_button.clicked.connect(self.prev_table)
    prev_param_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    
    #Middle Row Layout
    switch_graph_layout = QtWidgets.QHBoxLayout()
    switch_graph_layout.addWidget(prev_param_button)
    switch_graph_layout.addWidget(self.comp_table, alignment=Qt.AlignCenter)
    switch_graph_layout.addWidget(next_param_button)
    
    #Redisplay Ramp Button Settings
    redisplay_ramp_button = QtWidgets.QPushButton("Redisplay " + gpp_or_reco + " RAMP functions")
    redisplay_ramp_button.clicked.connect(self.redisplay_ramp_funcs)
    redisplay_ramp_button.setFixedSize(250,75)
    redisplay_ramp_button.setFont(QtGui.QFont("SansSerif", 9, QtGui.QFont.Bold))
    redisplay_ramp_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    
    if self.gpp_or_reco == "GPP":
      self.page_label = QtWidgets.QLabel("8. "+gpp_or_reco+" Optimized Parameter Differences")
      next_page = QtWidgets.QPushButton("Proceed")
      prev_page = QtWidgets.QPushButton("Re-select GPP \nOptimization Params")
    else:
      self.page_label = QtWidgets.QLabel("12. "+gpp_or_reco+" Optimized Parameter Differences")
      next_page = QtWidgets.QPushButton("Proceed")
      prev_page = QtWidgets.QPushButton("Re-select RECO \nOptimization Params")
    
    next_page.setFixedSize(250,75)
    prev_page.setFixedSize(250,75)
    next_page.setFont(QtGui.QFont("SansSerif", 9, QtGui.QFont.Bold))
    prev_page.setFont(QtGui.QFont("SansSerif", 9, QtGui.QFont.Bold))
    next_page.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    prev_page.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    
    self.page_label.setFont(QtGui.QFont("SansSerif", 13, QtGui.QFont.Bold))
    self.page_label.setAlignment(Qt.AlignCenter)
    self.pft_label = QtWidgets.QLabel("Current PFT: "+self.pft_chooser(1)) #TODO: change to get correct pft ind
    self.pft_label.setFont(QtGui.QFont("SansSerif", 11))
    self.pft_label.setAlignment(Qt.AlignCenter)
    self.current_graph_label = QtWidgets.QLabel("Showing Table " + str(self.current_param_plotted_index+1) + " of " + str(len(self.params)))
    self.current_graph_label.setFont(QtGui.QFont("SansSerif",11))
    self.current_graph_label.setAlignment(Qt.AlignCenter)

    next_page.clicked.connect(self.next_page)
    prev_page.clicked.connect(self.prev_page)
    
    bottom_layout = QtWidgets.QHBoxLayout()
    bottom_layout.addWidget(prev_page)
    bottom_layout.addWidget(redisplay_ramp_button)
    bottom_layout.addWidget(next_page)

    graph_layout = QtWidgets.QVBoxLayout()
    graph_layout.addWidget(self.page_label)
    graph_layout.addWidget(self.pft_label)
    graph_layout.addWidget(self.current_graph_label)
    graph_layout.addLayout(switch_graph_layout)
    graph_layout.addLayout(bottom_layout)

    self.setLayout(graph_layout)
    self.setWindowTitle(page_title)

  '''Remove later
  def decrement_current_param_plotted_index(self):
    if self.current_param_plotted_index == 0:
      self.current_param_plotted_index = len(self.param_to_data.keys()) - 1
    else:
      self.current_param_plotted_index -= 1
    self.plot_chosen_ramp_function()
    self.current_graph_label.setText("Showing graph " + str(self.current_param_plotted_index+1) + " of " + str(len(self.params)))

  def increment_current_param_plotted_index(self):
    if self.current_param_plotted_index == len(self.param_to_data.keys()) -1:
      self.current_param_plotted_index = 0
    else:
      self.current_param_plotted_index += 1
    self.plot_chosen_ramp_function()
    self.current_graph_label.setText("Showing graph " + str(self.current_param_plotted_index+1) + " of " + str(len(self.params)))
  '''
    
  def next_table(self):
    if self.current_param_plotted_index == len(self.param_to_data.keys()) -1:
      self.current_param_plotted_index = 0
    else:
      self.current_param_plotted_index += 1
    self.update_table()
    self.current_graph_label.setText("Showing Table " + str(self.current_param_plotted_index+1) + " of " + str(len(self.params)))
  
  def prev_table(self):
    if self.current_param_plotted_index == 0:
      self.current_param_plotted_index = len(self.param_to_data.keys()) - 1
    else:
      self.current_param_plotted_index -= 1
    self.update_table()
    self.current_graph_label.setText("Showing Table " + str(self.current_param_plotted_index+1) + " of " + str(len(self.params)))
 
  def update_table(self):
    self.current_param = self.params[self.current_param_plotted_index]
    self.comp_table.setItem(1,0,QtWidgets.QTableWidgetItem(self.gpp_or_reco + " vs " + self.current_param))
    self.comp_table.setItem(1,1,QtWidgets.QTableWidgetItem(str(self.param_to_data[self.current_param][0])))
    self.comp_table.setItem(1,2,QtWidgets.QTableWidgetItem(str(self.param_to_data[self.current_param][1])))
  
  '''Remove later
  def plot_chosen_ramp_function(self):
    current_param = self.params[self.current_param_plotted_index]
    data_to_plot = self.param_to_data[current_param]
    print(data_to_plot)
    ax = self.figure.add_subplot(111)
    ax.clear()
    ax.scatter(["Original","Updated Fit"], data_to_plot)
    ax.set_title(self.gpp_or_reco + " vs. " + current_param)
    ax.set_xlabel(current_param)
    ax.set_ylabel(self.gpp_or_reco)
    ax.set_ylim((-.1, 1.1))
    ax.plot((1, 0), (0, 0), color='orange', ls='dashed')
    ax.plot((0, 1), (1, 1), color='orange', ls='dashed')
    self.canvas.draw()
  '''
  
  def redisplay_ramp_funcs(self):
    self._ramp_page.show()
    self.hide()
  
  def set_pft(self,pft):
    self.pft = pft
    self.pft_label.setText("Current PFT: "+self.pft)
    self.next_page_ob.set_pft(pft)
