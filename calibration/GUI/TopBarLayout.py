from GUI.BasePage import *

class TopBarLayout(BasePage):
  
  def __init__(self, width, height):
    BasePage.__init__(self, width, height)  

    logo_label = QtWidgets.QLabel(self)
    logo_img = QtGui.QPixmap('GUI/images/NTSG_logo.jpg')
    logo_label.setPixmap(logo_img)

    filler_label = QtWidgets.QLabel(self)
    filler_img = QtGui.QPixmap('GUI/images/filler_img.jpg')
    filler_label.setPixmap(filler_img)
    
    main_layout = QtWidgets.QHBoxLayout()
    main_layout.addWidget(logo_label)
    # main_layout.addWidget(filler_label)
    self.setLayout(main_layout)
