import os
from typing import List, Optional

from .filter_absract import AbstractFileFilter


class FilterOnlyWithFilesExtension(AbstractFileFilter):
    """
    Filters out non-Python files by checking file extensions.
    """
    def __init__(self, include_only_extensions: Optional[List[str]] = None):
        self.include_only_extensions = include_only_extensions or []

    def _is_file_allowed(self, file: str) -> bool:
        """Checks if a single file is allowed based on its name."""
        _, ext = os.path.splitext(file)
        return ext in self.include_only_extensions

    def filter_files(self, files: List[str]) -> List[str]:
        """
        Filters files, allowing only those with the `.py` extension.

        Args:
            files (List[str]): A list of file paths.

        Returns:
            List[str]: Filtered list of Python files.
        """
        return [f for f in files if self._is_file_allowed(f)]

    def filter_dirs(self, dirs: List[str]) -> List[str]:
        """
        Allows all directories without filtering.

        Args:
            dirs (List[str]): A list of directory paths.

        Returns:
            List[str]: The unchanged list of directories.
        """
        return dirs