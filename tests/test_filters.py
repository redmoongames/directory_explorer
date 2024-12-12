import unittest
from src.services.project_scanner.filters.filter_absract import AbstractFileFilter
from src.services.project_scanner.filters.filter_exclude_directory import FilterExcludeDirectory
from src.services.project_scanner.filters.filter_exclude_file_extension import FilterExcludeFileExtension
from src.services.project_scanner.filters.filter_exclude_file_name import FilterExcludeFileName
from src.services.project_scanner.filters.filter_composite import FilterComposite

class TestFilterExcludeDirectory(unittest.TestCase):

    def test_filter_excludes_directories(self):
        filter = FilterExcludeDirectory(["__pycache__", ".secret"])

        expected = ["correct_1", "correct_2", "correct_3"]
        incorrect_directories = ["__pycache__", ".secret"]
        result = filter.filter_dirs(expected + incorrect_directories)
        self.assertEqual(expected, result)

        expected = ["/correct_1", "correct_2/", "./correct_3././", ]
        incorrect_directories = ["/__pycache__", ".secret/", "./.secret/./"]
        result = filter.filter_dirs(expected + incorrect_directories)
        self.assertEqual(expected, result)

        expected = ["a/correct_1/b/c", "/a/b/correct_2/c/d/"]
        incorrect_directories = ["a/b/__pycache__/b/c", "/a/b/.secret/c/d/"]
        result = filter.filter_dirs(expected + incorrect_directories)
        self.assertEqual(expected, result)

    def test_filter_allows_all_directories_when_empty(self):
        filter = FilterExcludeDirectory()
        expected = ["src", "node_modules", "tests"]
        result = filter.filter_dirs(expected)
        self.assertEqual(expected, result)

    def test_filter_does_not_affect_files(self):
        filter = FilterExcludeDirectory(["node_modules"])
        expected = ["file1.py", "file2.js"]
        result = filter.filter_files(expected)
        self.assertEqual(expected, result)

class TestFilterExcludeFileExtension(unittest.TestCase):

    def test_filter_excludes_file_extensions(self):
        filter = FilterExcludeFileExtension([".py", ".js"])
        files = ["file1.py", "file2.js", "file3.txt"]
        result = filter.filter_files(files)
        self.assertEqual(result, ["file3.txt"])

    def test_filter_allows_all_files_when_empty(self):
        filter = FilterExcludeFileExtension()
        files = ["file1.py", "file2.js", "file3.txt"]
        result = filter.filter_files(files)
        self.assertEqual(result, files)

    def test_filter_does_not_affect_directories(self):
        filter = FilterExcludeFileExtension([".py"])
        directories = ["src", "tests"]
        result = filter.filter_dirs(directories)
        self.assertEqual(result, directories)

class TestFilterExcludeFileName(unittest.TestCase):

    def test_filter_files_when_excludes_file_names(self):
        filter_exclude_dirs = FilterExcludeFileName(["secret.txt", "secrets.env"])

        expected = ["main.py", "secret.json", "public.txt", "_secrets.env"]
        incorrect_directories = ["secret.txt", "secrets.env"]
        result = filter_exclude_dirs.filter_files(expected + incorrect_directories)
        self.assertEqual(expected, result)

        expected = ["./main.py", "/secret.json", "public.txt/", "././_secrets.env././"]
        incorrect_directories = ["./secret.txt", "/secrets.env", "secret.txt/.", "secrets.env/"]
        result = filter_exclude_dirs.filter_files(expected + incorrect_directories)
        self.assertEqual(expected, result)

        expected = ["a/b/main.py", "/a/b/secret.json", "a/public.txt", "/a/_secrets.env"]
        incorrect_directories = ["a/b/secret.txt", "/a/b/secrets.env", "a/b/secret.txt/", "/a/b/secrets.env/"]
        result = filter_exclude_dirs.filter_files(expected + incorrect_directories)
        self.assertEqual(expected, result)

    def test_filter_allows_all_files_when_empty(self):
        filter = FilterExcludeFileName()
        files = ["main.py", "config.json", "app.js"]
        result = filter.filter_files(files)
        self.assertEqual(result, files)

    def test_filter_does_not_affect_directories(self):
        filter = FilterExcludeFileName(["config.json"])
        directories = ["src", "tests"]
        result = filter.filter_dirs(directories)
        self.assertEqual(result, directories)

class TestFilterComposite(unittest.TestCase):

    def test_composite_filters(self):
        directory_filter = FilterExcludeDirectory(["node_modules"])
        extension_filter = FilterExcludeFileExtension([".log"])
        name_filter = FilterExcludeFileName(["README.md"])

        composite_filter = FilterComposite([directory_filter, extension_filter, name_filter])

        directories = ["src", "node_modules", "tests"]
        files = ["main.py", "README.md", "error.log"]

        filtered_dirs = composite_filter.filter_dirs(directories)
        filtered_files = composite_filter.filter_files(files)

        self.assertEqual(filtered_dirs, ["src", "tests"])
        self.assertEqual(filtered_files, ["main.py"])

    def test_empty_composite_filter(self):
        composite_filter = FilterComposite([])

        directories = ["src", "node_modules", "tests"]
        files = ["main.py", "README.md", "error.log"]

        filtered_dirs = composite_filter.filter_dirs(directories)
        filtered_files = composite_filter.filter_files(files)

        self.assertEqual(filtered_dirs, directories)
        self.assertEqual(filtered_files, files)

if __name__ == "__main__":
    unittest.main()
