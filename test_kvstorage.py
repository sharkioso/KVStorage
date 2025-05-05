import unittest
from unittest.mock import patch
import io
from kvstorage import Storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.storage = Storage(size=3)

    def test_initialization(self):
        self.assertEqual(self.storage.size, 3)
        self.assertEqual(len(self.storage.table), 3)

    def test_str_representation(self):
        self.storage.add_key_value("key1", "value1")
        self.storage.add_key_value("key2", "value2")
        output = str(self.storage)
        self.assertIn("key1", output)
        self.assertIn("key2", output)

    def test_clean_storage(self):
        self.storage.add_key_value("key1", "value1")
        self.storage.clean_storage()
        self.assertTrue(all(len(bucket) == 0 for bucket in self.storage.table))

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_list_values(self, mock_stdout):
        self.storage.add_key_value("key1", "value1")
        self.storage.list_values()
        self.assertIn('значения в хранилище value1', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_none_key(self, mock_stdout):
        self.storage.add_key_value(None, "value")
        self.assertIn("не поддерживает хэширование", mock_stdout.getvalue())

    def test_hash_collision(self):
        self.storage = Storage(size=1)
        self.storage.add_key_value("key1", "value1")
        self.storage.add_key_value("key2", "value2")
        self.assertEqual(len(self.storage.table[0]), 2)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_key_operations(self, mock_stdout):
        """Тест для добавления, получения, обновления и удаления ключа"""
        # Добавление
        self.storage.add_key_value("key1", "value1")
        self.assertIn('Пара ключ-значение "key1: value1" добавлена.',
                      mock_stdout.getvalue())

        # Получение
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        self.storage.get_value("key1")
        self.assertIn('значение для ключа"key1": value1',
                      mock_stdout.getvalue())

        # Обновление
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        self.storage.add_key_value("key1", "new_value")
        self.assertIn('Ошибка: Ключ "key1" уже существует.',
                      mock_stdout.getvalue())

        # Удаление
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        self.storage.delete_key("key1")
        self.assertIn('Пара ключ-значение с ключом "key1" удалена.',
                      mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_magic_methods(self, mock_stdout):
        """Тест магических методов __setitem__ и __getitem__"""
        self.storage["magic_key"] = "magic_value"
        self.assertIn(
            'Пара ключ-значение "magic_key: magic_value" добавлена.',
            mock_stdout.getvalue())

        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        self.storage["magic_key"]
        self.assertIn('значение для ключа"magic_key": magic_value',
                      mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_nonexistent_key(self, mock_stdout):
        """Тест для несуществующих ключей"""
        self.storage.get_value("missing_key")
        self.assertIn('Ошибка: Ключ "missing_key" не найден.',
                      mock_stdout.getvalue())

        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        self.storage.delete_key("missing_key")
        self.assertIn('Ошибка: Ключ "missing_key" не найден.',
                      mock_stdout.getvalue())

    def test_hashing(self):
        """Тест хэширования"""
        # Валидный ключ
        key = "test_key"
        index = self.storage.hashing(key)
        self.assertIsInstance(index, int)
        self.assertTrue(0 <= index < self.storage.size)

        # Невалидный ключ
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.assertIsNone(self.storage.hashing([]))
            self.assertIn("не поддерживает хэширование",
                          mock_stdout.getvalue())

    def test_reinitialization(self):
        """Проверка повторного создания хранилища"""
        new_storage = Storage(size=5)
        self.assertEqual(new_storage.size, 5)
        self.assertEqual(len(new_storage.table), 5)


if __name__ == '__main__':
    unittest.main()
