from PyQt5.QtWidgets import QApplication, QTableWidgetItem
import unittest
from main import VariableManagerMain, get_variables, write_variable, delete_variable


class TestSwapItemsFunction(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.main_window = VariableManagerMain()

    def tearDown(self):
        self.app.exit()

    def test_swap_items(self):

        self.main_window.main_ui.tableWidget.setItem(0, 0, QTableWidgetItem("Item1"))
        self.main_window.main_ui.tableWidget.setItem(1, 0, QTableWidgetItem("Item2"))

        self.main_window.swap_items(0, 1)

        self.assertEqual(self.main_window.main_ui.tableWidget.takeItem(0, 0).text(), "Item2")
        self.assertEqual(self.main_window.main_ui.tableWidget.takeItem(1, 0).text(), "Item1")


if __name__ == '__main__':
    unittest.main()
