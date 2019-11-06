from BasePage import *

class GPPVsEmult(BasePage):

  def __init__(self, next_page_function, page_title):
    BasePage.__init__(self, next_page_function, page_title)

    data = [[random.random() for i in range(10)], [random.random() for j in range(10)]]
    self.figure = plt.figure()
    self.canvas = FigureCanvas(self.figure)
    self.toolbar = NavigationToolbar(self.canvas, self)

    ax = self.figure.add_subplot(111)
    ax.scatter(data[0], data[1])
    ax.set_title("GPP vs. Emult")
    ax.set_xlabel("Emult")
    ax.set_ylabel("GPP")
    self.canvas.draw()

    next_button = QtWidgets.QPushButton("Next")
    next_button.clicked.connect(self.next_page)

    main_layout = QtWidgets.QVBoxLayout()
    main_layout.addWidget(self.canvas)
    main_layout.addWidget(self.toolbar)
    main_layout.addWidget(next_button)
    self.setLayout(main_layout)
