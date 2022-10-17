import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

class Form(QMainWindow):
    def __init__(self) :
        super().__init__()
        self.ui = uic.loadUi("originUI.ui", self)
        self.ui.show()

    #Menu(파일)
    @pyqtSlot()
    def tmh_new_file(self):
        pass

    @pyqtSlot()
    def tmh_open_file(self):
        pass

    @pyqtSlot()
    def tmh_recent_file(self):
        pass

    @pyqtSlot()
    def tmh_save_this(self):
        pass

    @pyqtSlot()
    def tmh_custom_save(self):
        pass

    @pyqtSlot()
    def tmh_save_all(self):
        pass

    @pyqtSlot()
    def tmh_menu_close(self):
        pass

    #Menu(선택)
    @pyqtSlot()
    def tmh_set_workdir(self):
        pass

    @pyqtSlot()
    def tmh_set_type_code(self):
        pass

    #Menu(도움말)
    @pyqtSlot()
    def tmh_open_help(self):
        pass

    @pyqtSlot()
    def tmh_open_info(self):
        pass

    #파일 입력 영역
    @pyqtSlot()
    def tmh_open_file(self):
        pass

    @pyqtSlot()
    def tmh_check_data(self):
        pass

    #종의 정보 출력 영역
    @pyqtSlot()
    def tmh_change_type_code(self):
        pass

    #산정할 지수 선택
    @pyqtSlot()
    def tmh_calc_ambi(self):
        pass

    @pyqtSlot()
    def tmh_calc_isep(self):
        pass

    @pyqtSlot()
    def tmh_calc_sw_index(self):
        pass


if __name__ == "__main__" :
    app = QApplication(sys.argv)

    myWindow = Form()

    myWindow.show()

    app.exec_()
