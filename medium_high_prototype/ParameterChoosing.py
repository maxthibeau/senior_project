from BasePage import *

class ParameterChoosing(BasePage):

  def __init__(self, next_page_function, page_title, params):
    BasePage.__init__(self, next_page_function, page_title)

    self.params = params
    self.param_checkboxes = []

    for param in self.params:
      self.param_checkboxes.append(QtWidgets.QCheckBox(param))

    self.select_parameters_label = QtWidgets.QLabel("Select Parameters To Optimize:")
    self.select_parameters_label.setStyleSheet("text-decoration: underline;")

    grid_layout = QtWidgets.QGridLayout()
    for i in range(len(self.param_checkboxes)):
      param_checkbox = self.param_checkboxes[i]
      num_checkboxes = len(self.param_checkboxes)
      param_checkbox.setChecked(True)
      if i < num_checkboxes / 2:
        grid_layout.addWidget(param_checkbox, i, 0)
      else:
        grid_layout.addWidget(param_checkbox, i - num_checkboxes / 2, 1)

    self.optimize_button = QtWidgets.QPushButton("Optimize Parameters")
    self.optimize_button.clicked.connect(self.next_page)

    main_layout = QtWidgets.QHBoxLayout()
    main_layout.addWidget(self.select_parameters_label)
    main_layout.addLayout(grid_layout)
    main_layout.addWidget(self.optimize_button)
    self.setLayout(main_layout)


  def parameters_selected(self):
    for param_checkbox in self.param_checkboxes:
      if param_checkbox.isChecked():
        return True
    return False

  def parameters_to_optimize(self):
    params_to_optimize = []
    for param_checkbox in self.param_checkboxes:
      if param_checkbox.isChecked():
        params_to_optimize.append(param_checkbox.text())
    return params_to_optimize

  def next_page(self):
    if not self.parameters_selected():
      self.select_parameters_label.setText("Select At least one Parameter:")
      self.select_parameters_label.setStyleSheet("color: red; text-decoration: underline;")
    else:
      BasePage.next_page(self)
