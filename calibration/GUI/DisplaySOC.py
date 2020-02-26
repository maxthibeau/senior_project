from GUI.BasePage import *

class DisplaySOC(BasePage):

  def __init__(self, width, height, page_title):
    BasePage.__init__(self, width, height)

    data = [[random.random() for i in range(10)], [random.random() for j in range(10)]]
    self.figure = plt.figure()
    self.canvas = FigureCanvas(self.figure)
    self.toolbar = NavigationToolbar(self.canvas, self)

    ax = self.figure.add_subplot(111)
    ax.scatter(data[0], data[1])
    ax.set_title(page_title)
    x_axis, vs, y_axis = page_title.split()
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    self.canvas.draw()

    next_button = QtWidgets.QPushButton("Perform Numerical Spinups")
    prev_button = QtWidgets.QPushButton("Review RECO Parameter Difference")
    next_button.clicked.connect(self.next_page)
    prev_button.clicked.connect(self.prev_page)
    bottom_layout = QtWidgets.QHBoxLayout()
    bottom_layout.addWidget(prev_button)
    bottom_layout.addWidget(next_button)
    main_layout = QtWidgets.QVBoxLayout()
    main_layout.addWidget(self.canvas)
    main_layout.addWidget(self.toolbar)
    main_layout.addLayout(bottom_layout)
    self.setLayout(main_layout)
    self.setWindowTitle(page_title)
