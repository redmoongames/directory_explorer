from typing import List
from src.services.project_scanner.filters.filter_absract import AbstractFileFilter


class FilterComposite(AbstractFileFilter):
    """
    Combines multiple filters into one.

    Attributes:
        filters (List[AbstractFileFilter]): A list of filters to combine.
    """

    def __init__(self, filters: List[AbstractFileFilter]):
        """
        Initializes the composite filter with a list of filters.

        Args:
            filters (List[AbstractFileFilter]): A list of filters to combine.
        """
        self.filters = filters

    def filter_files(self, files: List[str]) -> List[str]:
        """
        Filters files using all combined filters.

        Args:
            files (List[str]): A list of file names.

        Returns:
            List[str]: The filtered list of files.
        """
        for filter_obj in self.filters:
            files = filter_obj.filter_files(files)
        return files

    def filter_dirs(self, dirs: List[str]) -> List[str]:
        """
        Filters directories using all combined filters.

        Args:
            dirs (List[str]): A list of directory names.

        Returns:
            List[str]: The filtered list of directories.
        """
        for filter_obj in self.filters:
            dirs = filter_obj.filter_dirs(dirs)
        return dirs