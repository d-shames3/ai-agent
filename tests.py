import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file
import os

class TestRunPythonFile(unittest.TestCase):
    def test_run_calculator_no_args(self):
        result = run_python_file("calculator", "main.py")
        print(result)
        expected = "STDOUT: b'Calculator App\\nUsage: python main.py \"<expression>\"\\nExample: python main.py \"3 + 5\"\\n\'\n"
        self.assertEqual(result, expected)

    def test_calculator_basic_args(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        expected = r"STDOUT: b'\xe2\x94\x8c\xe2\x94\x80\xe2\x94\x80\xe2\x94\x80\xe2\x94\x80\xe2\x94\x80\xe2\x94\x80\xe2\x94\x80\xe2\x94\x80\xe2\x94\x80\xe2\x94\x90\n\xe2\x94\x82  3 + 5  \xe2\x94\x82\n\xe2\x94\x82         \xe2\x94\x82\n\xe2\x94\x82  =      \xe2\x94\x82\n\xe2\x94\x82         \xe2\x94\x82\n\xe2\x94\x82  8      \xe2\x94\x82\n\xe2\x94\x94\xe2\x94\x80\xe2\x94\x80\xe2\x94\x80\xe2\x94\x80\xe2\x94\x80\xe2\x94\x80\xe2\x94\x80\xe2\x94\x80\xe2\x94\x80\xe2\x94\x98\n'" + "\n"
        print(result)
        self.assertEqual(result, expected)

    def test_calculator_dir_err(self):
        result = run_python_file("calculator", "../main.py")
        expected = 'Error: Cannot execute "../main.py" as it is outside the permitted working directory\n'
        print(result)
        self.assertEqual(result, expected)

    def test_calculator_file_err(self):
        result = run_python_file("calculator", "nonexistent.py")
        expected = 'Error: File "nonexistent.py" not found\n'
        print(result)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()