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
    self.next_page_ob = None
    self.prev_page_ob = None
  
  def set_next_page(self, next_page):
    self.next_page_ob = next_page

  def set_prev_page(self, prev_page):
    self.prev_page_ob = prev_page

  def prev_page(self):
    self.prev_window.connect(self.prev_page_ob.show)
    self.prev_window.emit()
    self.hide()
    
  #def next_page(self):
    #self.next_window.emit()
    #self.hide()

  def next_page(self,ind=-1):
    if (ind != -1):
        pft_ind = ind
        print("correct pft_ind of",pft_ind)
    self.next_window.connect(self.next_page_ob.show)
    self.next_window.emit()
    self.hide()

  def pft_chooser(self,ind):
     pfts = ["Evergreen Needleleaf","Evergreen Broadleaf","Deciduous Needleleaf","Deciduous Broadleaf","Shrub","Grass","Cereal Crop","Broadleaf Crop"]
     pft = pfts[ind]
     return pft
