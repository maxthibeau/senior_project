from GUI.BasePage import *

class ParameterDifference(BasePage):

  def __init__(self, width, height, page_title, optimized_params, gpp_or_reco, ramp_page):
    BasePage.__init__(self, width, height)

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

    self.figure = plt.figure()
    self.canvas = FigureCanvas(self.figure)
    self.toolbar = NavigationToolbar(self.canvas, self)
    self.plot_chosen_ramp_function()

    next_param_button = QtWidgets.QPushButton(">")
    next_param_button.setFixedSize(50,275)
    next_param_button.setToolTip('Go to next optimized ramp function')
    next_param_button.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
    next_param_button.clicked.connect(self.increment_current_param_plotted_index)
    prev_param_button = QtWidgets.QPushButton("<")
    prev_param_button.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
    prev_param_button.setFixedSize(50,275)
    prev_param_button.setToolTip('Go to previous optimized ramp function')
    prev_param_button.clicked.connect(self.decrement_current_param_plotted_index)
    
    switch_graph_layout = QtWidgets.QHBoxLayout()
    switch_graph_layout.addWidget(prev_param_button)
    switch_graph_layout.addWidget(self.canvas)
    switch_graph_layout.addWidget(next_param_button)

    redisplay_ramp_button = QtWidgets.QPushButton("Redisplay " + gpp_or_reco + " RAMP functions")
    redisplay_ramp_button.clicked.connect(self.redisplay_ramp_funcs)
    redisplay_ramp_button.setFixedSize(250,75)
    redisplay_ramp_button.setFont(QtGui.QFont("Times", 9, QtGui.QFont.Bold))
    if self.gpp_or_reco == "GPP":
      self.page_label = QtWidgets.QLabel("8. "+gpp_or_reco+" Optimized Parameter Differences")
      next_page = QtWidgets.QPushButton("Proceed")
      prev_page = QtWidgets.QPushButton("Re-select GPP Optimization Params")
    else:
      self.page_label = QtWidgets.QLabel("12. "+gpp_or_reco+" Optimized Parameter Differences")
      next_page = QtWidgets.QPushButton("Proceed")
      prev_page = QtWidgets.QPushButton("Re-select RECO Optimization Params")
    
    next_page.setFixedSize(250,75)
    prev_page.setFixedSize(250,75)
    next_page.setFont(QtGui.QFont("Times", 9, QtGui.QFont.Bold))
    prev_page.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
    self.page_label.setFont(QtGui.QFont("Times", 13))
    self.page_label.setAlignment(Qt.AlignCenter)
    self.pft_label = QtWidgets.QLabel("Current PFT: "+self.pft_chooser(1)) #TODO: change to get correct pft ind
    self.pft_label.setFont(QtGui.QFont("Times", 11))
    self.pft_label.setAlignment(Qt.AlignCenter)
    self.current_graph_label = QtWidgets.QLabel("Showing graph " + str(self.current_param_plotted_index+1) + " of " + str(len(self.params)))
    self.current_graph_label.setFont(QtGui.QFont("Times",11))
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
    graph_layout.addWidget(self.toolbar)
    graph_layout.addLayout(bottom_layout)

    self.setLayout(graph_layout)
    self.setWindowTitle(page_title)

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

  def plot_chosen_ramp_function(self):
    current_param = self.params[self.current_param_plotted_index]
    data_to_plot = self.param_to_data[current_param]
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

  def redisplay_ramp_funcs(self):
    self._ramp_page.show()
    self.hide()
