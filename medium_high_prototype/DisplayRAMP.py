from BasePage import *

class DisplayRAMP(BasePage):

  graph_gpp_vs_emult = QtCore.pyqtSignal()

  def __init__(self, graph_gpp_vs_emult_func, next_page_function, page_title, params_to_graph, gpp_or_reco):
    BasePage.__init__(self, next_page_function, page_title)

    self.graph_gpp_vs_emult.connect(graph_gpp_vs_emult_func)

    self.param_to_data = {}
    self.current_param_plotted_index = 0
    self.params = []
    for param in params_to_graph:
      self.params.append(param)
      self.param_to_data[param] = [[random.random() for i in range(10)], [random.random() for j in range(10)]]

    self.gpp_or_reco = gpp_or_reco      
    assert gpp_or_reco in ("GPP", "RECO")

    self.figure = plt.figure()
    self.canvas = FigureCanvas(self.figure)
    self.toolbar = NavigationToolbar(self.canvas, self)
    self.plot_chosen_ramp_function()

    next_ramp_button = QtWidgets.QPushButton("Next RAMP")
    prev_ramp_button = QtWidgets.QPushButton("Previous RAMP")
    next_ramp_button.clicked.connect(self.increment_current_param_plotted_index)
    prev_ramp_button.clicked.connect(self.decrement_current_param_plotted_index)
    switch_graph_layout = QtWidgets.QHBoxLayout()
    switch_graph_layout.addWidget(prev_ramp_button)
    switch_graph_layout.addWidget(next_ramp_button)

    choose_graph_gpp_vs_emult_label = QtWidgets.QLabel("Would you Like to graph GPP vs. Emult?")
    self.choose_graph_gpp_vs_emult = QtWidgets.QComboBox()
    self.choose_graph_gpp_vs_emult.addItems(["Yes", "No"])
    next_page = QtWidgets.QPushButton("Next")
    next_page.clicked.connect(self.next_page)

    bottom_layout = QtWidgets.QHBoxLayout()
    bottom_layout.addWidget(choose_graph_gpp_vs_emult_label)
    bottom_layout.addWidget(self.choose_graph_gpp_vs_emult)
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
    ax.scatter(data_to_plot[0], data_to_plot[1])
    ax.set_title(self.gpp_or_reco + " vs. " + current_param)
    ax.set_xlabel(current_param)
    ax.set_ylabel(self.gpp_or_reco)
    self.canvas.draw()
  
  def next_page(self):
    choose_graph_gpp_vs_emult = str(self.choose_graph_gpp_vs_emult.currentText())
    if choose_graph_gpp_vs_emult == "Yes":
      self.graph_gpp_vs_emult.emit()
      self.hide()
    else:
      BasePage.next_page(self)
