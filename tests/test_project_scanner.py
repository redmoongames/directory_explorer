import unittest
import os
from unittest.mock import patch, MagicMock
from src.services.project_scanner.project_scanner import ProjectScanner
from src.services.project_scanner.filters.filter_exclude_directory import FilterExcludeDirectory
from src.services.project_scanner.filters.filter_exclude_file_extension import FilterExcludeFileExtension
from src.services.project_scanner.filters.filter_exclude_file_name import FilterExcludeFileName
from src.services.project_scanner.models.directory_node import DirectoryNode


class TestProjectScanner(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory structure for testing."""
        self.test_root = "./test_project/"
        os.makedirs(self.test_root, exist_ok=True)

        # Create directories and files
        os.makedirs(os.path.join(self.test_root, "src", "nested"), exist_ok=True)
        os.makedirs(os.path.join(self.test_root, "tests"), exist_ok=True)
        os.makedirs(os.path.join(self.test_root, "node_modules"), exist_ok=True)

        with open(os.path.join(self.test_root, "main.py"), "w") as f:
            f.write("print('Hello World')")

        with open(os.path.join(self.test_root, "README.md"), "w") as f:
            f.write("# Project")

        with open(os.path.join(self.test_root, "src", "module.py"), "w") as f:
            f.write("def func(): pass")

        with open(os.path.join(self.test_root, "src", "nested", "nested_module.py"), "w") as f:
            f.write("def nested_func(): pass")

        with open(os.path.join(self.test_root, "tests", "test_module.py"), "w") as f:
            f.write("def test_func(): pass")

        # Create an unreadable file
        self.unreadable_file = os.path.join(self.test_root, "unreadable.txt")
        with open(self.unreadable_file, "w") as f:
            f.write("Unreadable content")
        os.chmod(self.unreadable_file, 0)

        # Filters
        self.base_filter = FilterExcludeDirectory(["node_modules"])
        self.scanner = ProjectScanner(self.test_root, self.base_filter)

    def tearDown(self):
        """Clean up the temporary directory after tests."""
        os.chmod(self.unreadable_file, 0o644)
        for root, dirs, files in os.walk(self.test_root, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_root)

    def test_fetch_structure_without_additional_filters(self):
        """Test fetching the directory structure without additional filters."""
        structure = self.scanner.fetch_structure()
        self.assertIsInstance(structure, DirectoryNode)
        self.assertEqual(structure.name, "test_project")
        self.assertIn("src", [d.name for d in structure.directories])
        self.assertNotIn("node_modules", [d.name for d in structure.directories])

    def test_fetch_structure_with_file_extension_filter(self):
        """Test fetching the structure with a file extension filter."""
        extension_filter = FilterExcludeFileExtension([".py"])
        structure = self.scanner.fetch_structure(additional_filter=extension_filter)
        src_dir = next((d for d in structure.directories if d.name == "src"), None)

        self.assertIsNotNone(src_dir)
        self.assertEqual(len(src_dir.files), 0)

    def test_fetch_structure_with_file_name_filter(self):
        """Test fetching the structure with a file name filter."""
        name_filter = FilterExcludeFileName(["README.md"])
        structure = self.scanner.fetch_structure(additional_filter=name_filter)

        self.assertNotIn("README.md", [f.name for f in structure.files])

    def test_fetch_structure_with_unreadable_file(self):
        """Test fetching structure with an unreadable file."""
        structure = self.scanner.fetch_structure()
        self.assertIn("unreadable.txt", [f.name for f in structure.files])
        unreadable_file = next((f for f in structure.files if f.name == "unreadable.txt"), None)
        self.assertEqual(unreadable_file.content, "<UNREADABLE: PermissionError>")

    def test_combined_filters(self):
        """Test fetching the structure with combined filters."""
        composite_filter = FilterExcludeFileExtension([".py", ".md"])
        structure = self.scanner.fetch_structure(additional_filter=composite_filter)

        self.assertNotIn("README.md", [f.name for f in structure.files])
        self.assertNotIn("module.py", [f.name for f in structure.files])

    def test_fetch_structure_deep_nesting(self):
        """Test fetching deeply nested directories and files."""
        structure = self.scanner.fetch_structure()
        src_dir = next((d for d in structure.directories if d.name == "src"), None)
        nested_dir = next((d for d in src_dir.directories if d.name == "nested"), None)

        self.assertIsNotNone(nested_dir)
        self.assertIn("nested_module.py", [f.name for f in nested_dir.files])

    def test_scan_empty_directory(self):
        """Test scanning an empty directory."""
        empty_dir = os.path.join(self.test_root, "empty_dir")
        os.makedirs(empty_dir)
        structure = self.scanner.fetch_structure(relative_path="empty_dir")

        self.assertEqual(len(structure.directories), 0)
        self.assertEqual(len(structure.files), 0)

    def test_invalid_path_raises_error(self):
        """Test that an invalid path raises a ValueError."""
        with self.assertRaises(ValueError):
            self.scanner.fetch_structure(relative_path="invalid_path")


if __name__ == "__main__":
    unittest.main()
