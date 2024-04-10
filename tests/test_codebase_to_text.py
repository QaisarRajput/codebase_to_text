import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from codebase_to_text.codebase_to_text import CodebaseToText
import shutil


class TestCodebaseToText(unittest.TestCase):
    def setUp(self):
        # Create a temporary folder with some test files
        self.test_folder_path = "test_folder"
        os.makedirs(self.test_folder_path, exist_ok=True)
        with open(os.path.join(self.test_folder_path, "test_file1.txt"), "w") as file:
            file.write("Test file 1 content")
        with open(os.path.join(self.test_folder_path, "test_file2.txt"), "w") as file:
            file.write("Test file 2 content")

    def test_get_text(self):
        code_to_text = CodebaseToText(input_path=self.test_folder_path, output_path="output.txt", output_type="txt")
        text = code_to_text.get_text()
        expected_text = f"Folder structure:\n{self.test_folder_path}/\n    test_file1.txt\n    test_file2.txt\n\nFile Contents:\n\n{self.test_folder_path}/test_file1.txt\nFile type: Text (.txt)\nTest file 1 content\n\n{self.test_folder_path}/test_file2.txt\nFile type: Text (.txt)\nTest file 2 content"
        self.assertEqual(text, expected_text)

    def tearDown(self):
        # Clean up temporary folder
        if os.path.exists(self.test_folder_path):
            shutil.rmtree(self.test_folder_path)

if __name__ == "__main__":
    print(sys.path)
    unittest.main()
