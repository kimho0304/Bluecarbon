import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

#form_class = uic.loadUiType("index.ui")[0]

#class Form(QMainWindow, form_class):
class Form(QMainWindow):
    def __init__(self) :
        super().__init__()
        self.ui = uic.loadUi("originUI.ui", self)
        #self.setupUi(self)
        self.ui.show()

    @pyqtSlot()
    def select(self):
        self.ui.lineEdit.setText("Test")

    @pyqtSlot()
    def validate(self):
        sys.exit()


if __name__ == "__main__" :
    app = QApplication(sys.argv)

    myWindow = Form()

    myWindow.show()

    app.exec_()
