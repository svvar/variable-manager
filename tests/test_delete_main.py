from unittest import TestCase, main
from unittest.mock import MagicMock, call

from main import VariableManagerMain
from main import delete_variable

class TestVariableManagerMain(TestCase):
    def test_delete_name_variable(self):
        # Створення об'єкта класу, який містить метод delete()
        # Може знадобитися ініціалізація об'єкту або створення умов для його виклику
        test_object = VariableManagerMain()

        # Умови для тестування, наприклад:
        test_object.main_ui.tableWidget.selectedItems.return_value = [MagicMock(text="TestName")]

        # Виклик методу delete()
        test_object.delete()

        # Перевірка на видалення змінної name
        self.assertTrue(delete_variable.called)
        self.assertEqual(delete_variable.call_args, call("TestName"))

    def test_load_data_after_delete(self):
        # Створення об'єкта класу, який містить метод delete()
        # Може знадобитися ініціалізація об'єкту або створення умов для його виклику
        test_object = VariableManagerMain()

        # Умови для тестування, наприклад:
        test_object.main_ui.tableWidget.selectedItems.return_value = [MagicMock(text="TestName")]

        # Виклик методу delete()
        test_object.delete()

        # Перевірка на виклик методу load_data()
        self.assertTrue(test_object.load_data.called)
        # Перевірка на виклик методу clearSelection()
        self.assertTrue(test_object.main_ui.tableWidget.clearSelection.called)
        # Перевірка на встановлення властивості pushButton_2
        self.assertTrue(test_object.main_ui.pushButton_2.setEnabled.called)
        self.assertEqual(test_object.main_ui.pushButton_2.setEnabled.call_args, call(False))

if __name__ == '__main__':
    main()

