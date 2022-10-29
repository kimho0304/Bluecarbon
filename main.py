import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
import pandas as pd
import numpy as np
import os
from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg

class TheGraph(QWidget):

    def __init__(self):
        super().__init__()

        pg.setConfigOptions(background='w')  # 배경 흰색으로.. ; global configuration options

        y = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

        y2 = [0, 1, 2, 4, 12, 14, 16, 17, 14, 22]

        x = range(0, 10)

        pw = pg.PlotWidget()

        pw.showGrid(x=True, y=True)

        pw.addLegend(
        size=(100, 10))  # LegendItem() 없으면, 생성후 반환 ; 매개변수는 LegendItem() 에서 사용 ==> size=(width,height)

        pw.setLabel("left", text="Value", units="v")  # PlotItem() 메소드

        pw.setLabel('bottom', text="Time", units='s')

        pw.setXRange(0, 10)  # 내부적으로 ViewBox() 메소드 사용함. -- setXRange(min, max, padding=None, update=True)

        pw.setYRange(0, 25)

        pw.plot(x, y, pen='b', symbol='x', symbolPen='g', symbolBrush=0.2, name='green')

        pw.plot(x, y2, pen='r', symbol='o', symbolPen='b', symbolBrush=0.2, name='blue')

        layout = QHBoxLayout()

        layout.addWidget(pw)

        self.setLayout(layout)

        self.setGeometry(300, 100, 550, 650)  # x, y, width, height

        self.setWindowTitle("pyqtgraph 예제 2")

class Form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("originUI.ui", self)
        self.ui.show()

    def tmh_show_graph(self):
        result_graph.show()

    # Menu(파일)
    @pyqtSlot()
    def tmh_new_file(self):
        self.tmh_inverse_SW_result.setRowCount(0)
        self.tmh_SW_result.setRowCount(0)
        self.tmh_standard_box_result.setRowCount(0)
        self.tmh_standard_box_outline.setRowCount(0)
        self.tmh_validate_box_result.setRowCount(0)
        self.tmh_validate_box_input.setText('')
        self.tmh_standard_box_Input.setText('')
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
        global excel_data2
        excel_data2.to_excel(fpath[0].replace('.xls', '_result.xls'), index=False)
        QMessageBox.information(self, 'Success!', '저장이 완료되었습니다.')
        pass

    @pyqtSlot()
    def tmh_custom_save(self):
        global excel_data2
        try:
            savepath = QFileDialog.getSaveFileName(self, '파일 저장', workdir, filter='Excel file(*xls *xlsx)')
        except NameError:
            savepath = QFileDialog.getSaveFileName(self, '파일 저장', filter='Excel file(*xls *xlsx)')
        if savepath[0] != '':
            excel_data2.to_excel(savepath[0].replace('.xlsx', '').replace('.xls', '') + '.xlsx', index=False)
            QMessageBox.information(self, 'Success!', '저장이 완료되었습니다.')

        pass

    @pyqtSlot()
    def tmh_save_all(self):
        pass

    @pyqtSlot()
    def tmh_menu_close(self):
        while (self.tmh_validate_box_result.rowCount() > 0):
            self.tmh_validate_box_result.removeRow(0)
        pass

    # Menu(선택)
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

            standard_data = pd.read_excel(standard_path[0], sheet_name=0)
            num0 = num1 = num2 = num3 = num4 = num5 = tot = 0

            global excel_data

            global ambi_list
            ambi_list = list()
            standard_list = list()
            base_list = list()

            for i in range(0, len(standard_data.index), 1):
                standard_list.append(standard_data['Name'][i])

            for i in range(1, len(excel_data.index), 1):
                base_list.append(excel_data['종명자료'][i])

            self.tmh_standard_box_result.setRowCount(len(excel_data.index) - 1)
            self.tmh_standard_box_outline.setRowCount(1)

            for i in range(7):
                self.tmh_standard_box_outline.setItem(0, i, QTableWidgetItem('0'))

            for j in range(0, len(excel_data.index) - 1, 1):
                try:
                    standard = standard_data['Group'][standard_list.index(excel_data['종명자료'][j + 1])]
                    self.tmh_standard_box_result.setItem(j, 0, QTableWidgetItem(str(base_list[j])))
                    if standard == 0:
                        standard = 2
                    self.tmh_standard_box_result.setItem(j, 1, QTableWidgetItem(str(standard)))
                except ValueError:
                    standard = 2  # 2로 고정
                    self.tmh_standard_box_result.setItem(j, 0, QTableWidgetItem(str(base_list[j])))
                    self.tmh_standard_box_result.setItem(j, 1, QTableWidgetItem(str(standard)))
                    self.tmh_standard_box_result.setItem(j, 2, QTableWidgetItem('신규'))

                excel_data['Group'][j] = standard

                if standard == 0:
                    excel_data['Group'][j] = 2
                    num2 += 1  # 미할당은 2로 교체
                    self.tmh_standard_box_outline.setItem(0, 6, QTableWidgetItem(str(num0)))
                elif standard == 1:
                    num1 += 1
                    self.tmh_standard_box_outline.setItem(0, 1, QTableWidgetItem(str(num1)))
                elif standard == 2:
                    num2 += 1
                    self.tmh_standard_box_outline.setItem(0, 2, QTableWidgetItem(str(num2)))
                elif standard == 3:
                    num3 += 1
                    self.tmh_standard_box_outline.setItem(0, 3, QTableWidgetItem(str(num3)))
                elif standard == 4:
                    num4 += 1
                    self.tmh_standard_box_outline.setItem(0, 4, QTableWidgetItem(str(num4)))
                elif standard == 5:
                    num5 += 1
                    self.tmh_standard_box_outline.setItem(0, 5, QTableWidgetItem(str(num5)))

                ambi_list.append(standard)

                tot += 1
                self.tmh_standard_box_outline.setItem(0, 0, QTableWidgetItem(str(tot)))

                QApplication.processEvents()

        pass

    # Menu(도움말)
    @pyqtSlot()
    def tmh_open_help(self):
        os.system('"' + os.getcwd() + '/help.html"')
        pass

    @pyqtSlot()
    def tmh_open_info(self):
        QMessageBox.about(self, '이 도구에 관하여', 'About Message')
        pass

    @pyqtSlot()
    def tmh_check_data(self):
        try:
            global excel_data
            excel_data = pd.read_excel(fpath[0], sheet_name=0)
            excel_data = excel_data.fillna(0)

            global excel_data2
            jj_count = len(excel_data2.index)

            self.tmh_validate_box_result.setRowCount(jj_count)

            num = 1
            while num <= jj_count:
                if num / 1000 >= 1:
                    N_num = 'N' + str(num)
                elif num / 100 >= 1:
                    N_num = 'N0' + str(num)
                elif num / 10 >= 1:
                    N_num = 'N00' + str(num)
                else:
                    N_num = 'N000' + str(num)

                self.tmh_validate_box_result.setItem(num - 1, 0, QTableWidgetItem(N_num))
                self.tmh_validate_box_result.setItem(num - 1, 1, QTableWidgetItem('정상'))

                num += 1

                QApplication.processEvents()

        except NameError:
            QMessageBox.information(self, 'Error!', '검증할 파일을 선택하지 않았습니다.')
        pass

    # 종의 정보 출력 영역
    @pyqtSlot()
    def tmh_change_type_code(self):
        pass

    # 산정할 지수 선택
    @pyqtSlot()
    def tmh_calc_ambi(self):
        global excel_data
        global excel_data2

        jj_count = len(excel_data2.index)

        self.tmh_AZTI_result.setRowCount(jj_count)

        global AMBI_list
        AMBI_list = list()

        num = 1

        while num <= jj_count:
            N = 0

            if num / 1000 >= 1:
                N_num = 'N' + str(num)
            elif num / 100 >= 1:
                N_num = 'N0' + str(num)
            elif num / 10 >= 1:
                N_num = 'N00' + str(num)
            else:
                N_num = 'N000' + str(num)

            self.tmh_AZTI_result.setItem(num - 1, 0, QTableWidgetItem(N_num))

            for i in range(2, len(excel_data.index), 1):
                N += excel_data[N_num][i]

            global ambi_list
            pG1 = pG2 = pG3 = pG4 = pG5 = 0
            sG1 = sG2 = sG3 = sG4 = sG5 = AMBI = 0.0

            for i in range(2, len(excel_data.index), 1):
                # AMBI
                if ambi_list[i - 2] == 1:
                    pG1 += excel_data[N_num][i]
                elif ambi_list[i - 2] == 2:
                    pG2 += excel_data[N_num][i]
                elif ambi_list[i - 2] == 3:
                    pG3 += excel_data[N_num][i]
                elif ambi_list[i - 2] == 4:
                    pG4 += excel_data[N_num][i]
                elif ambi_list[i - 2] == 5:
                    pG5 += excel_data[N_num][i]

            sG1 = pG1 / N * 100
            sG2 = pG2 / N * 100
            sG3 = pG3 / N * 100
            sG4 = pG4 / N * 100
            sG5 = pG4 / N * 100

            AMBI = ((0 * sG1) + (1.5 * sG2) + (3 * sG3) + (4.5 * sG4) + (6 * sG5)) / 100

            AMBI_list.append(AMBI)
            self.tmh_AZTI_result.setItem(num - 1, 1, QTableWidgetItem(str(AMBI)))

            num += 1
            status = 0

            if (status != int(num / jj_count * 100)):
                status = int(num / jj_count * 100)
                self.tmh_AZTI_bar.setValue(status)

            QApplication.processEvents()

        excel_data2['AMBI'] = ''
        for i in range(0, jj_count, 1):
            excel_data2['AMBI'][i] = AMBI_list[i]

        pass

    @pyqtSlot()
    def tmh_calc_isep(self):
        global excel_data2
        jj_count = len(excel_data2.index)

        self.tmh_inverse_SW_result.setRowCount(jj_count)

        global ISEP_list
        ISEP_list = list()

        num = 1

        while num <= jj_count:
            N = 0
            B = 0

            if num / 1000 >= 1:
                N_num = 'N' + str(num)
            elif num / 100 >= 1:
                N_num = 'N0' + str(num)
            elif num / 10 >= 1:
                N_num = 'N00' + str(num)
            else:
                N_num = 'N000' + str(num)

            self.tmh_inverse_SW_result.setItem(num - 1, 0, QTableWidgetItem(N_num))

            for i in range(2, len(excel_data.index), 1):
                N += excel_data[N_num][i]
                B += excel_data[N_num + '.1'][i]

            SEP_up = 0.0
            SEP_dn = 0.0

            for i in range(2, len(excel_data.index), 1):
                # ISEP 등급
                Ni = excel_data[N_num][i]
                Bi = excel_data[N_num + '.1'][i]
                Pi = Ni / N
                Pi_ = Bi / B

                SEP_up += Pi_ * np.log(Pi_, where=Pi_ > 0)
                SEP_dn += Pi * np.log(Pi, where=Pi > 0)

                if SEP_dn == 0.0:
                    ISEP = 0.0
                else:
                    SEP = -SEP_up / -SEP_dn
                    ISEP_n = (1 / SEP) + 1
                    ISEP = np.log10(ISEP_n, where=ISEP_n > 0)

            ISEP_list.append(ISEP)
            self.tmh_inverse_SW_result.setItem(num - 1, 1, QTableWidgetItem(str(ISEP)))

            num += 1
            status = 0

            if (status != int(num / jj_count * 100)):
                status = int(num / jj_count * 100)
                self.tmh_inverse_SW_bar.setValue(status)

            QApplication.processEvents()

        excel_data2['ISEP'] = ''
        for i in range(0, jj_count, 1):
            excel_data2['ISEP'][i] = ISEP_list[i]

        pass

    @pyqtSlot()
    def tmh_calc_sw_index(self):
        global excel_data2
        jj_count = len(excel_data2.index)
        self.tmh_SW_result.setRowCount(jj_count)

        global sw_ln_list
        global sw_log_list

        sw_ln_list = list()
        sw_log_list = list()

        num = 1

        while num <= jj_count:
            N = 0
            B = 0

            if num / 1000 >= 1:
                N_num = 'N' + str(num)
            elif num / 100 >= 1:
                N_num = 'N0' + str(num)
            elif num / 10 >= 1:
                N_num = 'N00' + str(num)
            else:
                N_num = 'N000' + str(num)

            self.tmh_SW_result.setItem(num - 1, 0, QTableWidgetItem(N_num))

            for i in range(2, len(excel_data.index), 1):
                N += excel_data[N_num][i]
                B += excel_data[N_num + '.1'][i]

            sw_ln = 0.0
            sw_log = 0.0

            for i in range(2, len(excel_data.index), 1):
                Ni = excel_data[N_num][i]
                Pi = Ni / N

                # Shannon-Wiener Index
                sw_ln -= Pi * np.log(Pi, where=Pi > 0)
                sw_log -= Pi * np.log2(Pi, where=Pi > 0)

            sw_ln_list.append(sw_ln)
            self.tmh_SW_result.setItem(num - 1, 1, QTableWidgetItem(str(sw_ln)))

            sw_log_list.append(sw_log)
            self.tmh_SW_result.setItem(num - 1, 2, QTableWidgetItem(str(sw_log)))

            num += 1
            status = 0

            if (status != int(num / jj_count * 100)):
                status = int(num / jj_count * 100)
                self.tmh_SW_bar.setValue(status)

            QApplication.processEvents()

        excel_data2['Shannon-Wiener Index (ln)'] = ''
        for i in range(0, jj_count, 1):
            excel_data2['Shannon-Wiener Index (ln)'][i] = sw_ln_list[i]

        excel_data2['Shannon-Wiener Index (log2)'] = ''
        for i in range(0, jj_count, 1):
            excel_data2['Shannon-Wiener Index (log2)'][i] = sw_log_list[i]

        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Form()
    myWindow.show()

    result_graph = TheGraph()
    app.exec_()