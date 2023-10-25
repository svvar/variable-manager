import enum
import os, sys

import PyQt5
from PyQt5.QtCore import QStringListModel, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QMessageBox

import createWindow, mainWindow, EditWindow
from PyQt5 import QtCore, QtGui, QtWidgets


class VariableManagerMain(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_ui = mainWindow.Ui_mainWindow()

        self.edit_window = VariableManagerEdit()
        self.creation_window = VariableManagerCreate()
        self.creation_window.creation_window_closed.connect(self.load_data)

        self.main_ui.setupUi(self)

        self.load_data()

        self.main_ui.lineEdit.textChanged.connect(self.auto_filter)
        self.main_ui.tableWidget.itemClicked.connect(self.enable_editing)
        self.main_ui.pushButton.clicked.connect(self.delete)
        self.main_ui.pushButton_2.clicked.connect(self.enter_edit_mode)
        self.main_ui.pushButton_3.clicked.connect(self.enter_create_mode)

    def load_data(self):
        data = dict(os.environ)
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

        self.edit_window.edit_ui.tableWidget.setRowCount(len(variable_values))

        # деякі значення можуть повторюватися у змінній, тому ітеруємо незвичним на перший погляд чином
        for n in range(len(variable_values)):
            self.edit_window.edit_ui.tableWidget.setItem(n, 0, QTableWidgetItem(variable_values[n]))
        self.edit_window.show()

    def enter_create_mode(self):
        self.creation_window.show()

    def delete(self):
        item = self.main_ui.tableWidget.selectedItems()[0]
        row = item.row()

        del os.environ[item.text()]

        self.load_data()
        self.main_ui.tableWidget.clearSelection()
        self.main_ui.pushButton_2.setEnabled(False)

    def swap_items(self, row1, row2):
        item1 = self.main_ui.tableWidget.takeItem(row1, 0)
        item2 = self.main_ui.tableWidget.takeItem(row2, 0)

        self.main_ui.tableWidget.setItem(row1, 0, item2)
        self.main_ui.tableWidget.setItem(row2, 0, item1)


class VariableManagerEdit(QMainWindow):
    def __init__(self):
        super().__init__()

        self.edit_ui = EditWindow.Ui_EditWindow()
        self.edit_ui.setupUi(self)

        self.edit_ui.tableWidget.clicked.connect(self.enable_buttons)
        self.edit_ui.pushButton.clicked.connect(self.add_value)
        self.edit_ui.pushButton_2.clicked.connect(self.edit_value)
        self.edit_ui.pushButton_3.clicked.connect(self.browse)
        self.edit_ui.pushButton_4.clicked.connect(self.delete)
        self.edit_ui.pushButton_5.clicked.connect(self.up)
        self.edit_ui.pushButton_6.clicked.connect(self.down)
        self.edit_ui.pushButton_8.clicked.connect(self.save)
        self.edit_ui.pushButton_9.clicked.connect(self.close)

    def enable_buttons(self):
        self.edit_ui.pushButton_2.setEnabled(True)
        self.edit_ui.pushButton_4.setEnabled(True)
        self.edit_ui.pushButton_5.setEnabled(True)
        self.edit_ui.pushButton_6.setEnabled(True)

    def disable_buttons(self):
        self.edit_ui.pushButton_2.setEnabled(False)
        self.edit_ui.pushButton_4.setEnabled(False)
        self.edit_ui.pushButton_5.setEnabled(False)
        self.edit_ui.pushButton_6.setEnabled(False)

    def add_value(self):
        self.enable_buttons()
        self.edit_ui.tableWidget.setRowCount(self.edit_ui.tableWidget.rowCount() + 1)
        row = self.edit_ui.tableWidget.rowCount() - 1
        self.edit_ui.tableWidget.setItem(row, 0, QTableWidgetItem())

        item = self.edit_ui.tableWidget.item(row, 0)

        self.edit_ui.tableWidget.editItem(item)

    def edit_value(self):
        item = self.edit_ui.tableWidget.selectedItems()[0]
        self.edit_ui.tableWidget.editItem(item)

    def browse(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

    def delete(self):
        # TODO Make it actually delete
        item = self.edit_ui.tableWidget.selectedItems()[0]
        row = item.row()
        while row < self.edit_ui.tableWidget.rowCount() - 1:
            self.swap_items(row, row + 1)
            row += 1

        self.edit_ui.tableWidget.setRowCount(self.edit_ui.tableWidget.rowCount() - 1)
        self.edit_ui.tableWidget.clearSelection()
        self.disable_buttons()

    def up(self):
        item = self.edit_ui.tableWidget.selectedItems()[0]

        row = item.row()
        if row > 0:
            self.swap_items(row, row - 1)
            self.edit_ui.tableWidget.item(row - 1, 0).setSelected(True)
            self.edit_ui.tableWidget.item(row, 0).setSelected(False)

    def down(self):
        item = self.edit_ui.tableWidget.selectedItems()[0]

        row = item.row()
        if row < self.edit_ui.tableWidget.rowCount() - 1:
            self.swap_items(row, row + 1)
            self.edit_ui.tableWidget.item(row + 1, 0).setSelected(True)
            self.edit_ui.tableWidget.item(row, 0).setSelected(False)

    def save(self):
        values = []

        for row in range(self.edit_ui.tableWidget.rowCount()):
            item = self.edit_ui.tableWidget.item(row, 0)
            text = item.text()
            if text != "" and not text.isspace():
                values.append(item.text())

        for row in values:
            print(row)

        # TODO REWRITE VARIABLE HERE

        self.close()

    def swap_items(self, row1, row2):
        item1 = self.edit_ui.tableWidget.takeItem(row1, 0)
        item2 = self.edit_ui.tableWidget.takeItem(row2, 0)

        self.edit_ui.tableWidget.setItem(row1, 0, item2)
        self.edit_ui.tableWidget.setItem(row2, 0, item1)


class VariableManagerCreate(QMainWindow):
    creation_window_closed = PyQt5.QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.create_ui = createWindow.Ui_SecondWindow()
        self.create_ui.setupUi(self)


        self.create_ui.lineEdit.textChanged.connect(self.update_button)
        self.create_ui.lineEdit_2.textChanged.connect(self.update_button)
        self.create_ui.pushButton.clicked.connect(self.save_variable)
        # self.create_ui.pushButton_2.clicked.connect(pass)
        # self.create_ui.pushButton_3.connect(self.browse)
        self.create_ui.pushButton_4.clicked.connect(self.close)

    def update_button(self):
        line1 = self.create_ui.lineEdit.text()
        line2 = self.create_ui.lineEdit_2.text()

        if line1 != "" and line2 != "":
            self.create_ui.pushButton.setEnabled(True)
        else:
            self.create_ui.pushButton.setEnabled(False)

    def save_variable(self):
        name = self.create_ui.lineEdit.text()
        value = self.create_ui.lineEdit_2.text()

        os.environ[name] = value
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.creation_window_closed.emit()
        super().closeEvent(a0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VariableManagerMain()
    window.show()
    sys.exit(app.exec_())
