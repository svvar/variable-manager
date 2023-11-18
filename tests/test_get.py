import unittest
from unittest.mock import mock_open, patch
from main import get_variables


class TestGetVariablesFunction(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="VAR1=value1\nVAR2=value2\n")
    def test_get_variables_from_file(self, mock_file):
        # Очікуваний результат
        expected_result = {'VAR1': 'value1', 'VAR2': 'value2'}

        # Виклик функції, яку тестуємо
        result = get_variables()

        # Перевірка на співпадіння з очікуваним результатом
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
