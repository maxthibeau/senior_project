from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class BasePage(QtWidgets.QDialog):

  next_window = QtCore.pyqtSignal()
  prev_window = QtCore.pyqtSignal()

  def __init__(self, width, height):
    QtWidgets.QWidget.__init__(self)
    self.setGeometry(300, 300, width, height)

  def set_next_page(self, next_page):
    self.next_window.connect(next_page.show)

  def set_prev_page(self, prev_page):
    self.prev_window.connect(prev_page.show)

  def prev_page(self):
    self.prev_window.emit()
    self.hide()

  def next_page(self):
    self.next_window.emit()
    self.hide()
