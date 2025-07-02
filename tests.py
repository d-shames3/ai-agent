import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
import os

class TestGetFilesInfo(unittest.TestCase):
    
    def test_pkg_dir(self):
        results = get_files_info("calculator", "pkg")
        expected = "Results for pkg directory:\n- render.py: file_size=754 bytes, is_dir=False\n- __pycache__: file_size=128 bytes, is_dir=True\n- calculator.py: file_size=1721 bytes, is_dir=False\n"
        print(results)
        self.assertEqual(results, expected)
    
    def test_calculator_dir(self):
        results = get_files_info("calculator", ".")
        expected = "Results for calculator directory:\n- tests.py: file_size=1331 bytes, is_dir=False\n- main.py: file_size=565 bytes, is_dir=False\n- pkg: file_size=160 bytes, is_dir=True\n"
        print(results)
        self.assertEqual(results, expected)

    def test_bin_dir(self):
        results = get_files_info("calculator", "/bin")
        expected = "Error: Cannot list /bin as it is outside the permitted working directory"
        print(results)
        self.assertEqual(results, expected)

    def test_different_directory(self):
        results = get_files_info("calculator", "../")
        print(results)
        expected = "Error: Cannot list ../ as it is outside the permitted working directory"
        self.assertEqual(results, expected)

class TestGetFileContent(unittest.TestCase):

    def test_main(self):
        results = get_file_content("calculator", "main.py")
        print(results)
        cwd = os.getcwd()
        file_path = os.path.abspath(os.path.join(cwd, "calculator/main.py"))
        with open(file_path, "r") as f:
            raw_file = f.read(10000)
        self.assertEqual(results, raw_file)

    def test_calculator(self):
        results = get_file_content("calculator/pkg", "calculator.py")
        print(results)
        cwd = os.getcwd()
        file_path = os.path.abspath(os.path.join(cwd, "calculator/pkg/calculator.py"))
        with open(file_path, "r") as f:
            raw_file = f.read(10000)
        self.assertEqual(results, raw_file)

    def test_bin(self):
        results = get_file_content("calculator", "/bin/cat")
        print(results)
        expected = "Error: Cannot read /bin/cat as it is outside the permitted working directory"
        self.assertEqual(results, expected)

if __name__ == "__main__":
    unittest.main()