import unittest
from unittest.mock import mock_open, patch
from main import delete_variable


class TestDeleteVariableFunction(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="VAR1=value1\nVAR2=value2\n")
    def test_delete_existing_variable(self, mock_file):
        name = 'VAR1'
        delete_variable(name)
        mock_file.assert_called_with('.env', 'w')
        mock_file().write.assert_called_with("VAR2=value2\n")

    @patch('builtins.open', new_callable=mock_open, read_data="VAR1=value1\nVAR2=value2\n")
    def test_delete_nonexistent_variable(self, mock_file):
        name = 'VAR3'
        delete_variable(name)
        mock_file.assert_called_with('.env', 'w')
        mock_file().write.assert_called_with("VAR1=value1\nVAR2=value2\n")

    @patch('builtins.open', new_callable=mock_open, read_data="")
    def test_delete_from_empty_file(self, mock_file):
        name = 'VAR1'
        delete_variable(name)
        mock_file.assert_called_with('.env', 'w')
        mock_file().write.assert_called_with("")


if __name__ == '__main__':
    unittest.main()
