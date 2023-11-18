import unittest
from unittest.mock import mock_open, patch
from main import write_variable


class TestWriteVariableFunction(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="VAR1=old_value\nVAR2=old_value\n")
    def test_write_existing_variable(self, mock_file):
        name = 'VAR1'
        value = 'new_value'
        write_variable(name, value)
        mock_file.assert_called_with('.env', 'w')
        mock_file().write.assert_called_with("VAR1=new_value\nVAR2=old_value\n")

    @patch('builtins.open', new_callable=mock_open, read_data="VAR1=old_value\nVAR2=old_value\n")
    def test_write_new_variable(self, mock_file):
        name = 'VAR3'
        value = 'new_value'
        write_variable(name, value)
        mock_file.assert_called_with('.env', 'w')
        mock_file().write.assert_called_with("VAR1=old_value\nVAR2=old_value\nVAR3=new_value\n")

    @patch('builtins.open', new_callable=mock_open, read_data="VAR1=old_value\nVAR2=old_value\n")
    def test_write_existing_variable_multiple_times(self, mock_file):
        name = 'VAR2'
        value = 'new_value'
        write_variable(name, value)
        mock_file.assert_called_with('.env', 'w')
        mock_file().write.assert_called_with("VAR1=old_value\nVAR2=new_value\n")

    @patch('builtins.open', new_callable=mock_open, read_data="")
    def test_write_empty_file(self, mock_file):
        name = 'VAR1'
        value = 'new_value'
        write_variable(name, value)
        mock_file.assert_called_with('.env', 'w')
        mock_file().write.assert_called_with("VAR1=new_value\n")


if __name__ == '__main__':
    unittest.main()
