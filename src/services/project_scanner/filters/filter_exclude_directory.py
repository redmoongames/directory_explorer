import os
from typing import List, Optional

from .filter_absract import AbstractFileFilter


class FilterExcludeDirectory(AbstractFileFilter):
    """
    Filters directories based on their names.

    Attributes:
        excluded_dirs (Optional[List[str]]): A list of directory names to exclude.
    """

    def __init__(self, excluded_dirs: Optional[List[str]] = None):
        """
        Initializes the filter with the list of directory names to exclude.

        Args:
            excluded_dirs (Optional[List[str]]): A list of directory names to exclude. Defaults to None.
        """
        self.excluded_dirs = set(excluded_dirs) if excluded_dirs else set()

    def _is_directory_allowed(self, directory: str) -> bool:
        """
        Checks if a single directory is allowed based on its components.

        Args:
            directory (str): Directory path to check.

        Returns:
            bool: True if none of the components of the path are in the exclusion list, False otherwise.
        """
        components = os.path.normpath(directory).split(os.sep)
        return not any(component in self.excluded_dirs for component in components)

    def filter_files(self, files: List[str]) -> List[str]:
        """
        Always allows all files without filtering.

        Args:
            files (List[str]): A list of file names.

        Returns:
            List[str]: The unchanged list of files.
        """
        return files

    def filter_dirs(self, dirs: List[str]) -> List[str]:
        """
        Filters directories by excluding those with specific names.

        Args:
            dirs (List[str]): A list of directory paths.

        Returns:
            List[str]: Filtered list of directories.
        """
        return [d for d in dirs if self._is_directory_allowed(d)]
