from abc import abstractmethod, ABC

from src import DirectoryNode


class FormatterAbstract(ABC):
    """
    Abstract base class for output formatters.
    """

    @abstractmethod
    def format(self, directory_node: DirectoryNode) -> str:
        """
        Formats a DirectoryNode into a specific string representation.

        Args:
            directory_node (DirectoryNode): The directory structure to format.

        Returns:
            str: The formatted representation of the directory structure.
        """
        pass
