import matplotlib.pyplot as plt
import numpy as np
import math

# The Ramp class is used to plot ramp functions
class Ramp():
  def __init__(self,x_min_val,x_max_val,y_min_val,y_max_val,x_label,y_label,title):
    x_scale = x_max_val - x_min_val
    x_margin = x_scale / 10
    plt.plot([x_min_val-x_margin,x_min_val,x_max_val,x_max_val+x_margin],[y_min_val,y_min_val,y_max_val,y_max_val])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

# The Arrhenious function is used for f(TSOIL)
def Arrhenious(tsoil,b_tsoil):
  # (1/66.02) = 0.0151469252
  return math.exp(b_tsoil*(0.0151469252-(1/(tsoil-227.13))))
  
