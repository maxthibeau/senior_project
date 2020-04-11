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

    next_ramp_button = QtWidgets.QPushButton(">")
    prev_ramp_button = QtWidgets.QPushButton("<")
    next_ramp_button.setFixedSize(50,275)
    prev_ramp_button.setFixedSize(50,275)
    next_ramp_button.setFont(QtGui.QFont("SansSerif", 12, QtGui.QFont.Bold))
    prev_ramp_button.setFont(QtGui.QFont("SansSerif", 12, QtGui.QFont.Bold))
    next_ramp_button.clicked.connect(self.increment_current_param_plotted_index)
    prev_ramp_button.clicked.connect(self.decrement_current_param_plotted_index)
    next_ramp_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    prev_ramp_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    if self.gpp_or_reco == "GPP":
      self.ramp_label = QtWidgets.QLabel("6. "+self.gpp_or_reco+" Ramp Functions")
      next_page = QtWidgets.QPushButton("Proceed")
      prev_page = QtWidgets.QPushButton("Back")
    else: #self.gpp_or_reco == "RECO"
      self.ramp_label = QtWidgets.QLabel("10. "+self.gpp_or_reco+" Ramp Functions")
      next_page = QtWidgets.QPushButton("Proceed")
      prev_page = QtWidgets.QPushButton("Back")
    
    next_page.setFixedSize(250,75)
    prev_page.setFixedSize(250,75)
    next_page.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    prev_page.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    next_page.setFont(QtGui.QFont("SansSerif", 9, QtGui.QFont.Bold))
    prev_page.setFont(QtGui.QFont("SansSerif", 9, QtGui.QFont.Bold))
    
    self.ramp_label.setFont(QtGui.QFont("SansSerif", 13))
    self.ramp_label.setAlignment(Qt.AlignCenter)
    self.pft_label = QtWidgets.QLabel("Current PFT: "+self.pft_chooser(1)) #TODO: change to get correct pft ind
    self.pft_label.setFont(QtGui.QFont("SansSerif", 11))
    self.pft_label.setAlignment(Qt.AlignCenter)
    self.current_graph_label = QtWidgets.QLabel("Showing graph " + str(self.current_param_plotted_index+1) + " of " + str(len(self.params)))
    self.current_graph_label.setFont(QtGui.QFont("SansSerif",11))
    self.current_graph_label.setAlignment(Qt.AlignCenter)

    optional_graph_button = QtWidgets.QPushButton("Plot " + optional_graph_name + " (optional)")
    optional_graph_button.clicked.connect(self._optional_graph_widget.show)
    optional_graph_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    optional_graph_button.setFixedSize(250,75)
    optional_graph_button.setFont(QtGui.QFont("SansSerif", 9, QtGui.QFont.Bold))
    next_page.clicked.connect(self.next_page)
    prev_page.clicked.connect(self.prev_page)
    
    # layout
    canvas_layout = QtWidgets.QHBoxLayout()
    canvas_layout.addWidget(prev_ramp_button)
    canvas_layout.addWidget(self.canvas)
    canvas_layout.addWidget(next_ramp_button)
    
    toolbar_layout = QtWidgets.QHBoxLayout()
    toolbar_layout.setAlignment(Qt.AlignCenter)
    toolbar_layout.addWidget(self.toolbar)
    
    bottom_layout = QtWidgets.QHBoxLayout()
    bottom_layout.addWidget(prev_page)
    bottom_layout.addWidget(optional_graph_button)
    bottom_layout.addWidget(next_page)

    graph_layout = QtWidgets.QVBoxLayout()
    graph_layout.addWidget(self.ramp_label)
    graph_layout.addWidget(self.pft_label)
    graph_layout.addWidget(self.current_graph_label)
    graph_layout.addLayout(canvas_layout)
    graph_layout.addLayout(toolbar_layout)
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
    ax.scatter(data_to_plot[0], data_to_plot[1])
    ax.set_title(self.gpp_or_reco + " vs. " + current_param)
    ax.set_xlabel(current_param)
    ax.set_ylabel(self.gpp_or_reco)
    self.canvas.draw()
    
