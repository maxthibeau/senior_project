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

    next_param_button = QtWidgets.QPushButton("Next RAMP Function")
    next_param_button.setToolTip('Go to next optimized ramp function')
    next_param_button.clicked.connect(self.increment_current_param_plotted_index)
    prev_param_button = QtWidgets.QPushButton("Previous RAMP Function")
    prev_param_button.setToolTip('Go to previous optimized ramp function')
    prev_param_button.clicked.connect(self.decrement_current_param_plotted_index)
    switch_graph_layout = QtWidgets.QHBoxLayout()
    switch_graph_layout.addWidget(prev_param_button)
    switch_graph_layout.addWidget(next_param_button)

    redisplay_ramp_button = QtWidgets.QPushButton("Redisplay " + gpp_or_reco + " RAMP functions (optional)")
    redisplay_ramp_button.clicked.connect(self.redisplay_ramp_funcs)
    if self.gpp_or_reco == "GPP":
      self.page_label = QtWidgets.QLabel("8. "+gpp_or_reco+" Optimized Parameter Differences")
      next_page = QtWidgets.QPushButton("Optimize RECO Params")
      prev_page = QtWidgets.QPushButton("Re-select GPP Optimization Params")
    else:
      self.page_label = QtWidgets.QLabel("12. "+gpp_or_reco+" Optimized Parameter Differences")
      next_page = QtWidgets.QPushButton("Plot empirical vs. computed SOC")
      prev_page = QtWidgets.QPushButton("Re-select RECO Optimization Params")
    self.page_label.setFont(QtGui.QFont("Times", 13))
    self.page_label.setAlignment(Qt.AlignCenter)

    next_page.clicked.connect(self.next_page)
    prev_page.clicked.connect(self.prev_page)

    bottom_layout = QtWidgets.QHBoxLayout()
    bottom_layout.addWidget(prev_page)
    bottom_layout.addWidget(redisplay_ramp_button)
    bottom_layout.addWidget(next_page)

    graph_layout = QtWidgets.QVBoxLayout()
    graph_layout.addWidget(self.page_label)
    graph_layout.addWidget(self.canvas)
    graph_layout.addWidget(self.toolbar)
    graph_layout.addLayout(switch_graph_layout)
    graph_layout.addLayout(bottom_layout)

    self.setLayout(graph_layout)
    self.setWindowTitle(page_title)

  def decrement_current_param_plotted_index(self):
    if self.current_param_plotted_index == 0:
      self.current_param_plotted_index = len(self.param_to_data.keys()) - 1
    else:
      self.current_param_plotted_index -= 1
    self.plot_chosen_ramp_function()

  def increment_current_param_plotted_index(self):
    if self.current_param_plotted_index == len(self.param_to_data.keys()) -1:
      self.current_param_plotted_index = 0
    else:
      self.current_param_plotted_index += 1
    self.plot_chosen_ramp_function()

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
