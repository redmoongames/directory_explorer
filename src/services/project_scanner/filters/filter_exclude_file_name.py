import os
from typing import List, Optional

from src import AbstractFileFilter


class FilterExcludeFileName(AbstractFileFilter):
    """
    Filters out files with specific names.

    Attributes:
        excluded_names (Optional[List[str]]): A list of file names to exclude.
    """

    def __init__(self, excluded_names: Optional[List[str]] = None):
        """
        Initializes the filter with the list of file names to exclude.

        Args:
            excluded_names (Optional[List[str]]): A list of file names to exclude. Defaults to None.
        """
        self.excluded_names = set(excluded_names) if excluded_names else set()

    def _is_file_allowed(self, file: str) -> bool:
        """Checks if a single file is allowed based on its name."""
        file_name = os.path.basename(os.path.normpath(file))
        return file_name not in self.excluded_names

    def filter_files(self, files: List[str]) -> List[str]:
        """
        Filters files by excluding those with specific names.

        Args:
            files (List[str]): A list of file names.

        Returns:
            List[str]: Filtered list of files.
        """
        return [f for f in files if self._is_file_allowed(f)]

    def filter_dirs(self, dirs: List[str]) -> List[str]:
        """
        Always allows directories without filtering.

        Args:
            dirs (List[str]): A list of directory names.

        Returns:
            List[str]: The unchanged list of directories.
        """
        return dirs
