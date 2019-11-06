from PyQt5 import QtCore, QtWidgets, QtGui
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import random

class BasePage(QtWidgets.QDialog):

  next_window = QtCore.pyqtSignal()

  def __init__(self, next_page_function, page_title):
    QtWidgets.QWidget.__init__(self)
    if next_page_function != None:
      self.next_window.connect(next_page_function)

    self.setWindowTitle(page_title)

  def next_page(self):
    self.next_window.emit()
    self.hide()
