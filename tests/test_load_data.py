from PyQt5.QtWidgets import QApplication
import unittest
from unittest.mock import MagicMock, patch
from main import VariableManagerMain, get_variables, write_variable, delete_variable


class TestLoadDataFunction(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.main_window = VariableManagerMain()

    def tearDown(self):
        self.app.exit()

    @patch("main.get_variables")
    def test_load_data(self, mock_get_variables: MagicMock):

        mock_get_variables.return_value = {"VAR1": "VALUE1", "VAR2": "VALUE2", "VAR3": "VALUE3",
                                           "VAR4": "VALUE4", "VAR5": "VALUE5"}

        self.main_window.load_data()

        table_variables = []

        for row in range(self.main_window.main_ui.tableWidget.rowCount()):
            table_variables.append((self.main_window.main_ui.tableWidget.item(row, 0).text(),
                                   self.main_window.main_ui.tableWidget.item(row, 1).text()))

        file_variables = mock_get_variables()

        for key in file_variables:
            self.assertIn((key, file_variables[key]), table_variables)


if __name__ == '__main__':
    unittest.main()
