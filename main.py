import os, sys

from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QMessageBox

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
        self.main_ui.pushButton.clicked.connect(self.delete)
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

    def delete(self):
        item = self.main_ui.tableWidget.selectedItems()[0]
        row = item.row()
        while row < self.main_ui.tableWidget.rowCount() - 1:
            self.swap_items(row, row + 1)
            row += 1

        self.main_ui.tableWidget.setRowCount(self.main_ui.tableWidget.rowCount() - 1)
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
        self.edit_ui.pushButton_9.clicked.connect(self.close_window)

    def close_window(self):
        self.close()

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

        self.close_window()

    def swap_items(self, row1, row2):
        item1 = self.edit_ui.tableWidget.takeItem(row1, 0)
        item2 = self.edit_ui.tableWidget.takeItem(row2, 0)

        self.edit_ui.tableWidget.setItem(row1, 0, item2)
        self.edit_ui.tableWidget.setItem(row2, 0, item1)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VariableManagerMain()
    window.show()
    sys.exit(app.exec_())
