from GUI.BasePage import *

class SmoothOutliers(BasePage):

  def __init__(self, width, height, page_title, gpp_or_reco, tooltips):
    BasePage.__init__(self, width, height)
    tooltip = tooltips
    self.data_smoothed = False

    self.gpp_or_reco = gpp_or_reco
    assert self.gpp_or_reco in ("GPP", "RECO")

    # graph outlier data
    self.data_before_outlier_removal = [random.random() for i in range(10)]
    self.data_after_outlier_removal = []

    self.figure, self.axes = plt.subplots(2, 1)
    self.canvas = FigureCanvas(self.figure)
    self.toolbar = NavigationToolbar(self.canvas, self)
    self.draw_plot()

    # display number of outliers rmoeved
    self.outlier_label = QtWidgets.QLabel(self.gpp_or_reco)
    if(self.gpp_or_reco == "GPP"):
        self.outlier_label.setToolTip(tooltip["GPP"])
    else: # self.gpp_or_reco == "RECO"
        self.outlier_label.setToolTip(tooltip["RECO"])
    self.num_outliers_removed_label = QtWidgets.QLabel(" # of outliers removed: 5")
    self.elements_removed_layout = QtWidgets.QHBoxLayout()
    self.elements_removed_layout.addWidget(self.outlier_label)
    self.elements_removed_layout.addWidget(self.num_outliers_removed_label)

    # let user select smoothing parameters
    self.smoothing_selection_label = QtWidgets.QLabel('Select Smoothing Parameters:')
    self.smoothing_selection_label.setStyleSheet("text-decoration: underline;")

    self.window_selector_label = QtWidgets.QLabel("Window Type:")
    self.window_selector = QtWidgets.QComboBox()
    self.window_selector.addItems(["flat", "hanning" "hamming", "bartlett", "blackman"])

    self.window_size_label = QtWidgets.QLabel("Window Size (needs to be a float > 0):")
    self.window_size = QtWidgets.QLineEdit(self)
    self.window_size.setPlaceholderText("Required")

    self.smoothing_selection_layout = QtWidgets.QHBoxLayout()
    self.smoothing_selection_layout.addWidget(self.window_selector_label)
    self.smoothing_selection_layout.addWidget(self.window_selector)
    self.smoothing_selection_layout.addWidget(self.window_size_label)
    self.smoothing_selection_layout.addWidget(self.window_size)

    # give user navigation abilities
    smooth_button = QtWidgets.QPushButton("Smooth Data")
    smooth_button.setToolTip('Remove outliers (spikes) in the flux tower GPP')
    if self.gpp_or_reco == "RECO":
      next_page = QtWidgets.QPushButton("Optimize GPP")
      prev_page = QtWidgets.QPushButton("Re-smooth GPP")
    else:
      next_page = QtWidgets.QPushButton("Smooth RECO Outliers")
      prev_page = QtWidgets.QPushButton("Re-Select PFT")

    smooth_button.clicked.connect(self.smooth_data)
    next_page.clicked.connect(self.next_page)
    prev_page.clicked.connect(self.prev_page)

    self.bottom_layout = QtWidgets.QHBoxLayout()
    self.bottom_layout.addWidget(prev_page)
    self.bottom_layout.addWidget(smooth_button)
    self.bottom_layout.addWidget(next_page)

    # combine all elements into one layout
    grid_layout = QtWidgets.QVBoxLayout()
    grid_layout.addWidget(self.canvas)
    grid_layout.addWidget(self.toolbar)
    grid_layout.addLayout(self.elements_removed_layout)
    grid_layout.addWidget(self.smoothing_selection_label)
    grid_layout.addLayout(self.smoothing_selection_layout)
    grid_layout.addLayout(self.bottom_layout)
    self.setLayout(grid_layout)
    self.setWindowTitle(page_title)

  def draw_plot(self):
    for ax in self.axes:
      ax.clear()
    plt.subplots_adjust(hspace=.4)
    self.axes[0].hist(self.data_before_outlier_removal)
    self.axes[0].set_title(self.gpp_or_reco + ' Before Outlier Smoothing')
    self.axes[1].hist(self.data_after_outlier_removal)
    self.axes[1].set_title(self.gpp_or_reco + ' After Outlier Smoothing')
    self.canvas.draw()

  def get_window_size(self):
    window_size_input = self.window_size.text()
    try:
      float(window_size_input)
    except ValueError:
      self.window_size_label.setStyleSheet("color: red;")
      return
    if float(window_size_input) < 0:
      self.window_size_label.setStyleSheet("color: red;")
      return
    self.window_size_label.setStyleSheet("color: black;")
    return window_size_input

  def smooth_data(self):
    if self.get_window_size() != None:
      self.data_smoothed = True
      self.data_after_outlier_removal = [random.random() for i in range(10)]
      self.draw_plot()

  def next_page(self):
    if self.data_smoothed:
      self.window_size_label.setStyleSheet("color: black;")
      self.next_window.emit()
      self.close()
    else:
      self.window_size_label.setStyleSheet("color: red;")
      
