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
        working_dir = self.ops.working_dir
        self.ops._validate_path = working_dir
        self.assertTrue(os.path.exists(os.path.join(self.ops.current_path)))
                    

if __name__ == "__main__":
    unittest.main()