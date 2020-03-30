from GUI.BasePage import *

class DisplayRAMP(BasePage):

  def __init__(self, width, height, page_title, gpp_or_reco, params_to_graph, optional_graph_widget, optional_graph_name):
    BasePage.__init__(self, width, height)

    self._optional_graph_widget = optional_graph_widget

    self.param_to_data = {}
    self.current_param_plotted_index = 0
    # generate some random data
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

    next_ramp_button = QtWidgets.QPushButton("Next RAMP Function")
    prev_ramp_button = QtWidgets.QPushButton("Previous RAMP Function")
    next_ramp_button.clicked.connect(self.increment_current_param_plotted_index)
    prev_ramp_button.clicked.connect(self.decrement_current_param_plotted_index)
    switch_graph_layout = QtWidgets.QHBoxLayout()
    switch_graph_layout.addWidget(prev_ramp_button)
    switch_graph_layout.addWidget(next_ramp_button)

    if self.gpp_or_reco == "GPP":
      self.ramp_label = QtWidgets.QLabel("6. "+self.gpp_or_reco+" Ramp Functions")
      next_page = QtWidgets.QPushButton("Choose GPP Optimization Params")
      prev_page = QtWidgets.QPushButton("Re-Smooth RECO Outliers")
    else: #self.gpp_or_reco == "RECO"
      self.ramp_label = QtWidgets.QLabel("10. "+self.gpp_or_reco+" Ramp Functions")
      next_page = QtWidgets.QPushButton("Choose RECO Optimization Params")
      prev_page = QtWidgets.QPushButton("Prev")
    self.ramp_label.setFont(QtGui.QFont("Times", 13))
    self.ramp_label.setAlignment(Qt.AlignCenter)
    self.pft_label = QtWidgets.QLabel("Current PFT: "+self.pft_chooser(1)) #TODO: change to get correct pft ind
    self.pft_label.setFont(QtGui.QFont("Times", 11))
    self.pft_label.setAlignment(Qt.AlignCenter)

    optional_graph_button = QtWidgets.QPushButton("Plot " + optional_graph_name + " (optional)")
    optional_graph_button.clicked.connect(self._optional_graph_widget.show)
    next_page.clicked.connect(self.next_page)
    prev_page.clicked.connect(self.prev_page)
    # layout
    bottom_layout = QtWidgets.QHBoxLayout()
    bottom_layout.addWidget(prev_page)
    bottom_layout.addWidget(optional_graph_button)
    bottom_layout.addWidget(next_page)

    graph_layout = QtWidgets.QVBoxLayout()
    graph_layout.addWidget(self.ramp_label)
    graph_layout.addWidget(self.pft_label)
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
    ax.scatter(data_to_plot[0], data_to_plot[1])
    ax.set_title(self.gpp_or_reco + " vs. " + current_param)
    ax.set_xlabel(current_param)
    ax.set_ylabel(self.gpp_or_reco)
    self.canvas.draw()
