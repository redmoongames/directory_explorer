from abc import ABC, abstractmethod
from typing import List, Dict


class ContextStorage(ABC):
    """
    Abstract base class for message context storage.

    This class defines the interface for saving and loading message contexts.
    Implementations should provide concrete storage mechanisms, such as file-based
    or database-backed solutions.
    """

    @abstractmethod
    def save_messages(self, messages: List[Dict[str, str]]) -> None:
        """
        Saves a list of messages to the storage.

        Args:
            messages (List[Dict[str, str]]): A list of message dictionaries to save.
                Each message should include the keys "role" and "content".

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Subclasses must implement 'save_messages'.")

    @abstractmethod
    def load_messages(self) -> List[Dict[str, str]]:
        """
        Loads a list of messages from the storage.

        Returns:
            List[Dict[str, str]]: A list of message dictionaries loaded from the storage.
                Each message should include the keys "role" and "content".

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Subclasses must implement 'load_messages'.")
