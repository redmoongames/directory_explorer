from abc import ABC, abstractmethod
from typing import List


class AbstractFileFilter(ABC):
    """Abstract base class for file and directory filters."""

    @abstractmethod
    def filter_files(self, files: List[str]) -> List[str]:
        """Filters files and returns the allowed ones."""
        pass

    @abstractmethod
    def filter_dirs(self, dirs: List[str]) -> List[str]:
        """Filters directories and returns the allowed ones."""
        pass