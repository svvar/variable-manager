import os, sys

from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

import createWindow, mainWindow, EditWindow
from PyQt5 import QtCore, QtGui, QtWidgets


class VariableManagerMain(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_ui = mainWindow.Ui_mainWindow()

        self.main_ui.setupUi(self)

        self.load_data(dict(os.environ))

        self.main_ui.lineEdit.textChanged.connect(self.auto_filter)
        self.main_ui.tableWidget.itemClicked.connect(self.enable_editing)
        self.main_ui.pushButton_2.clicked.connect(self.enter_edit_mode)

    def load_data(self, data):
        table = self.main_ui.tableWidget
        table.setRowCount(len(data))

        for e in data:
            row = list(data).index(e)
            table.setItem(row, 0, QTableWidgetItem(e))
            table.setItem(row, 1, QTableWidgetItem(data[e]))

    def auto_filter(self, text: str):
        visible_rows = []
        row_count = self.main_ui.tableWidget.rowCount()

        for row in range(row_count):
            if text.strip().upper() in self.main_ui.tableWidget.item(row, 0).text():
                visible_rows.append(row)

        for row in range(row_count):
            self.main_ui.tableWidget.setRowHidden(row, True)

        if text == "":
            visible_rows = [i for i in range(row_count)]

        for row in visible_rows:
            self.main_ui.tableWidget.setRowHidden(row, False)

    def enable_editing(self, item):
        self.main_ui.pushButton_2.setEnabled(True)

    def enter_edit_mode(self):
        selected_variable_content = self.main_ui.tableWidget.selectedItems()[1].text()
        variable_values = selected_variable_content.split(';')

        self.edit_window = VariableManagerEdit()
        self.edit_window.edit_ui.tableWidget.setRowCount(len(variable_values))

        # деякі значення можуть повторюватися у змінній, тому ітеруємо незвичним на перший погляд чином
        for n in range(len(variable_values)):
            self.edit_window.edit_ui.tableWidget.setItem(n, 0, QTableWidgetItem(variable_values[n]))
        self.edit_window.show()



class VariableManagerEdit(QMainWindow):
    def __init__(self):
        super().__init__()

        self.edit_ui = EditWindow.Ui_EditWindow()
        self.edit_ui.setupUi(self)

        self.edit_ui.pushButton_9.clicked.connect(self.close_window)


    def close_window(self):
        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VariableManagerMain()
    window.show()
    sys.exit(app.exec_())







