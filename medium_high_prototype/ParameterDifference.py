from BasePage import *

class ParameterDifference(BasePage):

  redisplay_ramp = QtCore.pyqtSignal()

  def __init__(self, redisplay_ramp_function, next_page_function, page_title, optimized_params, gpp_or_reco):
    BasePage.__init__(self, next_page_function, page_title)

    self.redisplay_ramp.connect(redisplay_ramp_function)

    self.optimized_params = optimized_params

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

    next_param_button = QtWidgets.QPushButton("Next RAMP")
    prev_param_button = QtWidgets.QPushButton("Previous RAMP")
    next_param_button.clicked.connect(self.increment_current_param_plotted_index)
    prev_param_button.clicked.connect(self.decrement_current_param_plotted_index)
    switch_graph_layout = QtWidgets.QHBoxLayout()
    switch_graph_layout.addWidget(prev_param_button)
    switch_graph_layout.addWidget(next_param_button)

    choose_redisplay_ramp_label = QtWidgets.QLabel("Would you Like to Redisplay " + gpp_or_reco + " RAMP functions?")
    self.choose_redisplay_ramp = QtWidgets.QComboBox()
    self.choose_redisplay_ramp.addItems(["Yes", "No"])
    next_page = QtWidgets.QPushButton("Next")
    next_page.clicked.connect(self.next_page)

    bottom_layout = QtWidgets.QHBoxLayout()
    bottom_layout.addWidget(choose_redisplay_ramp_label)
    bottom_layout.addWidget(self.choose_redisplay_ramp)
    bottom_layout.addWidget(next_page)

    graph_layout = QtWidgets.QVBoxLayout()
    graph_layout.addWidget(self.canvas)
    graph_layout.addWidget(self.toolbar)
    graph_layout.addLayout(switch_graph_layout)
    graph_layout.addLayout(bottom_layout)

    self.setLayout(graph_layout)
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

  def next_page(self):
    redisplay_ramp_choice = str(self.choose_redisplay_ramp.currentText())
    if redisplay_ramp_choice == "Yes":
      self.redisplay_ramp.emit()
      self.hide()
    else:
      BasePage.next_page(self)
