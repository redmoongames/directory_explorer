import os
from typing import List, Optional

from .filter_absract import AbstractFileFilter


class FilterExcludeFileExtension(AbstractFileFilter):
    """
    Filters files based on their extensions.

    Attributes:
        excluded_extensions (Optional[List[str]]): A list of file extensions to exclude.
    """

    def __init__(self, excluded_extensions: Optional[List[str]] = None):
        """
        Initializes the filter with the list of file extensions to exclude.

        Args:
            excluded_extensions (Optional[List[str]]): A list of file extensions to exclude. Defaults to None.
        """
        self.excluded_extensions = set(excluded_extensions) if excluded_extensions else set()

    def _is_file_allowed(self, file: str) -> bool:
        """Checks if a single file is allowed based on its extension."""
        _, ext = os.path.splitext(file)
        return ext not in self.excluded_extensions

    def filter_files(self, files: List[str]) -> List[str]:
        """
        Filters files by excluding those with specific extensions.

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