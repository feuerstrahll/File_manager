import unittest
import os
import shutil
from src.operations import Operations

class TestOperations(unittest.TestCase):
    def setUp(self):
        self.ops = Operations()

    def test_create_folder(self):
        folder_name = "test_folder"
        self.ops.create_folder(folder_name)
        self.assertTrue(os.path.exists(os.path.join(self.ops.current_path, folder_name)))

    def test_create_file(self):
        file_name = "test_file.txt"
        self.ops.create_file(file_name)
        self.assertTrue(os.path.exists(os.path.join(self.ops.current_path, file_name)))

    def test_validate_path(self):
        valid_path = os.path.join(self.ops.working_dir, "test_folder")
        result = self.ops._validate_path(valid_path)
        self.assertEqual(result, os.path.abspath(valid_path))

        # Проверка недопустимого пути (выход за пределы рабочей директории)
        invalid_path = os.path.abspath(os.path.join(self.ops.working_dir, "../hack"))
        with self.assertRaises(PermissionError):
            self.ops._validate_path(invalid_path)

    def test_get_relative_path(self):
        abs_path = os.path.join(self.ops.working_dir, "test_folder")
        rel_path = self.ops._get_relative_path(abs_path)
        self.assertEqual(rel_path, "test_folder")

    def test_navigation_safety(self):
        # Попытка выйти за пределы рабочей директории
        with self.assertRaises(PermissionError):
            self.ops.navigate("in", "../")
                        

if __name__ == "__main__":
    unittest.main()