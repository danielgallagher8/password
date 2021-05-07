"""
Password Keeper application to store passwords locally
"""

#Import libraries
from PyQt5 import QtWidgets
import sys

#Define classes
class App(QtWidgets.QMainWindow):
  
  def __init__(self, *args, **kwargs):
    super(App, self).__init__(*args, **kwargs)
    self.initial_layout()
  
  def initial_layout(self):
    pass

def run():
  app = QtWidgets.QApplication(sys.argv)
  win = App()
  win.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  run()
