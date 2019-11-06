from BasePage import *

class Plot():
  def __init__(self, plt, fig_num, parent):
    
    self.figure = plt.figure(fig_num)
    self.canvas = FigureCanvas(self.figure)
    self.toolbar = NavigationToolbar(self.canvas, parent)    

  def layout(self, plt_function, plt_args):
    ax = self.figure.add_subplot()
    plt_function(*plt_args)
    self.canvas.draw()
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(self.canvas)
    layout.addWidget(self.toolbar)
    return layout
