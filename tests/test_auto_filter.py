from PyQt5.QtWidgets import QApplication
import unittest
from unittest.mock import MagicMock
from main import VariableManagerMain, get_variables, write_variable, delete_variable


class TestAutoFilterFunction(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.main_window = VariableManagerMain()

    def tearDown(self):
        self.app.exit()

    def test_auto_filter_empty_text(self):

        self.main_window.main_ui.tableWidget.rowCount = MagicMock(return_value=5)
        item_mock = MagicMock()
        item_mock.text.return_value = "TEST ITEM"
        self.main_window.main_ui.tableWidget.item = MagicMock(return_value=item_mock)

        self.main_window.auto_filter("")

        for row in range(self.main_window.main_ui.tableWidget.rowCount()):
            self.assertFalse(self.main_window.main_ui.tableWidget.isRowHidden(row),
                             f'Row {str(self.main_window.main_ui.tableWidget.item(row, 0).text())} is hidden')

    def test_auto_filter_matching_text(self):

        self.main_window.main_ui.tableWidget.rowCount = MagicMock(return_value=3)
        item_mock = MagicMock()
        item_mock.text.return_value = "TEST ITEM"
        self.main_window.main_ui.tableWidget.item = MagicMock(return_value=item_mock)

        self.main_window.auto_filter("Test")

        for row in range(self.main_window.main_ui.tableWidget.rowCount()):
            self.assertEqual(self.main_window.main_ui.tableWidget.isRowHidden(row), False,
                             f'Row {str(self.main_window.main_ui.tableWidget.item(row, 0).text())} is hidden')

    def test_auto_filter_not_matching_text(self):

        self.main_window.main_ui.tableWidget.rowCount = MagicMock(return_value=3)
        item_mock = MagicMock()
        item_mock.text.return_value = "TEST ITEM"
        self.main_window.main_ui.tableWidget.item = MagicMock(return_value=item_mock)

        self.main_window.auto_filter("abcd")

        for row in range(self.main_window.main_ui.tableWidget.rowCount()):
            self.assertEqual(self.main_window.main_ui.tableWidget.isRowHidden(row), True,
                             f'Row {str(self.main_window.main_ui.tableWidget.item(row, 0).text())} is not hidden')


if __name__ == '__main__':
    unittest.main()
