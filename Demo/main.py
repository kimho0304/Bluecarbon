import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
import pandas as pd
import numpy as np
import operator
from functools import WRAPPER_ASSIGNMENTS, reduce
import time
import os

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
        global fpath
        try:
            fpath = QFileDialog.getOpenFileName(self, '파일 선택', workdir, filter='Excel file(*xls *xlsx)')    
        except NameError:
            fpath = QFileDialog.getOpenFileName(self, '파일 선택', filter='Excel file(*xls *xlsx)')
        
        if fpath[0] != '':
            global excel_data2
            excel_data2 = pd.read_excel(fpath[0], sheet_name=1)

            self.tmh_validate_box_input.setText(fpath[0])

        pass

    @pyqtSlot()
    def tmh_recent_file(self):
        pass

    @pyqtSlot()
    def tmh_save_this(self):
        excel_data3.to_excel(fpath, index=False)
        pass

    @pyqtSlot()
    def tmh_custom_save(self):
        pass

    @pyqtSlot()
    def tmh_save_all(self):
        pass

    @pyqtSlot()
    def tmh_menu_close(self):
        while (self.tableFriends.rowCount() > 0):
            self.tableFriends.removeRow(0)
        pass

    #Menu(선택)
    @pyqtSlot()
    def tmh_set_workdir(self):
        global workdir
        workdir = QFileDialog.getExistingDirectory(self, "작업 디렉토리 선택")
        pass

    @pyqtSlot()
    def tmh_set_type_code(self):
        global standard_path
        try:
            standard_path = QFileDialog.getOpenFileName(self, '파일 선택', workdir, filter='Excel file(*xls *xlsx)')    
        except NameError:
            standard_path = QFileDialog.getOpenFileName(self, '파일 선택', filter='Excel file(*xls *xlsx)')
        
        if standard_path[0] != '':
            self.tmh_standard_box_Input.setText(standard_path[0])
            
        pass

    #Menu(도움말)
    @pyqtSlot()
    def tmh_open_help(self):
        os.system('"'+os.getcwd()+'/help.html"')
        pass

    @pyqtSlot()
    def tmh_open_info(self):
        QMessageBox.about(self,'이 도구에 관하여','About Message')
        pass

    @pyqtSlot()
    def tmh_check_data(self):
        try:
            global excel_data
            excel_data = pd.read_excel(fpath[0], sheet_name=0)
            excel_data = excel_data.fillna(0)

            self.tmh_validate_box_result.setItem(0, 0, QTableWidgetItem('test'))

        except NameError:
            QMessageBox.information(self,'Error!','검증할 파일을 선택하지 않았습니다.')
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
        global excel_data2
        jj_count = len(excel_data2.index)

        global ISEP_list
        ISEP_list = list()

        num = 1

        while num < jj_count:
            N = 0
            B = 0

            if num / 1000 >= 1:
                N_num = 'N'+str(num)
            elif num / 100 >= 1:
                N_num = 'N0'+str(num)
            elif num / 10 >= 1:
                N_num = 'N00'+str(num)
            else:
                N_num = 'N000'+str(num)

            for i in range(2, len(excel_data.index), 1):
                N += excel_data[N_num][i]
                B += excel_data[N_num+'.1'][i]

            SEP_up = 0.0
            SEP_dn = 0.0

            for i in range(2, len(excel_data.index), 1):
                #ISEP 등급
                Ni = excel_data[N_num][i]
                Bi = excel_data[N_num+'.1'][i]
                Pi = Ni / N
                Pi_ = Bi / B

                SEP_up += Pi_ * np.log(Pi_, where = Pi_ > 0)
                SEP_dn += Pi * np.log(Pi, where = Pi > 0)

                if SEP_dn == 0.0:
                    ISEP = 0.0
                else:
                    SEP = -SEP_up / -SEP_dn
                    ISEP_n = (1 / SEP) + 1
                    ISEP = np.log10(ISEP_n, where = ISEP_n > 0)
		
            ISEP_list.append(ISEP)
            #print(sw_log)

            num += 1
            status = 0
            
            if(status != int(num/jj_count*100)):
                status = int(num/jj_count*100)
                self.tmh_inverse_SW_bar.setValue(status)
        pass

    @pyqtSlot()
    def tmh_calc_sw_index(self):
        global excel_data2
        jj_count = len(excel_data2.index)

        global sw_ln_list
        global sw_log_list

        sw_ln_list = list()
        sw_log_list = list()

        num = 1

        while num < jj_count:
            N = 0
            B = 0

            if num / 1000 >= 1:
                N_num = 'N'+str(num)
            elif num / 100 >= 1:
                N_num = 'N0'+str(num)
            elif num / 10 >= 1:
                N_num = 'N00'+str(num)
            else:
                N_num = 'N000'+str(num)

            for i in range(2, len(excel_data.index), 1):
                N += excel_data[N_num][i]
                B += excel_data[N_num+'.1'][i]

            sw_ln = 0.0
            sw_log = 0.0

            for i in range(2, len(excel_data.index), 1):
                Ni = excel_data[N_num][i]
                Pi = Ni / N

                #Shannon-Wiener Index
                sw_ln -= Pi * np.log(Pi, where = Pi > 0)
                sw_log -= Pi * np.log2(Pi, where = Pi > 0)

            #print(N_num)
            sw_ln_list.append(sw_ln)
            #print(sw_ln)
            sw_ln_list.append(sw_log)
            #print(sw_log)

            num += 1
            status = 0
            
            if(status != int(num/jj_count*100)):
                status = int(num/jj_count*100)
                self.tmh_SW_bar.setValue(status)
            
        pass

if __name__ == "__main__" :
    app = QApplication(sys.argv)

    myWindow = Form()

    myWindow.show()

    app.exec_()
