import json
from typing import List, Dict, Optional
from datetime import datetime

from src.services.context_service.context_storage import ContextStorage


class ContextService:
    """
    Service for managing a message context.

    This service allows adding, removing, exporting, and importing messages in a format compatible with OpenAI API.
    """

    def __init__(self, storage_service: ContextStorage):
        """
        Initializes the ContextService.

        Args:
            storage_service (ContextStorage): The storage backend for messages.
        """
        self._messages: List[Dict[str, str]] = []
        self._storage_service = storage_service
        self._load_from_storage()

    def _load_from_storage(self) -> None:
        """
        Loads messages from the storage backend.
        """
        try:
            self._messages = self._storage_service.load_messages()
        except Exception as e:
            raise RuntimeError(f"Failed to load messages from storage: {e}")

    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None) -> None:
        """
        Adds a new message to the context.

        Args:
            role (str): The role of the message ("system", "user", "assistant").
            content (str): The content of the message.
            metadata (Optional[Dict]): Additional metadata for the message.

        Raises:
            ValueError: If the role is invalid or content is empty.
        """
        if role not in {"system", "user", "assistant"}:
            raise ValueError(f"Invalid role '{role}'. Allowed roles are: 'system', 'user', 'assistant'.")
        if not content.strip():
            raise ValueError("Content cannot be empty.")

        message = {
            "role": role,
            "content": content.strip(),
            "timestamp": datetime.utcnow().isoformat(),
        }
        if metadata:
            message["metadata"] = metadata

        self._messages.append(message)
        self._save_to_storage()

    def get_all_messages(self) -> List[Dict[str, str]]:
        """
        Retrieves all messages in the context.

        Returns:
            List[Dict[str, str]]: A list of all messages.
        """
        return self._messages

    def get_last_n_messages(self, n: int) -> List[Dict[str, str]]:
        """
        Retrieves the last N messages.

        Args:
            n (int): The number of messages to retrieve.

        Returns:
            List[Dict[str, str]]: A list of the last N messages.
        """
        return self._messages[-n:] if n > 0 else []

    def remove_message(self, index: int) -> None:
        """
        Removes a message by its index.

        Args:
            index (int): The index of the message to remove.

        Raises:
            IndexError: If the index is out of range.
        """
        if not (0 <= index < len(self._messages)):
            raise IndexError("Message index out of range.")
        del self._messages[index]
        self._save_to_storage()

    def clear_context(self) -> None:
        """
        Clears all messages from the context.
        """
        self._messages = []
        self._save_to_storage()

    def export_to_json(self) -> str:
        """
        Exports the context to a JSON string.

        Returns:
            str: A JSON string representation of the messages.
        """
        return json.dumps(self._messages, indent=2)

    def import_from_json(self, json_data: str) -> None:
        """
        Imports messages from a JSON string.

        Args:
            json_data (str): A JSON string containing the messages.

        Raises:
            ValueError: If the JSON format is invalid or the data is not a list of messages.
        """
        try:
            messages = json.loads(json_data)
            if not isinstance(messages, list):
                raise ValueError("Imported data must be a list of messages.")
            for message in messages:
                if not isinstance(message, dict) or "role" not in message or "content" not in message:
                    raise ValueError("Each message must be a dictionary with 'role' and 'content' fields.")
            self._messages = messages
            self._save_to_storage()
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")

    def _save_to_storage(self) -> None:
        """
        Saves the current messages to the storage backend.
        """
        try:
            self._storage_service.save_messages(self._messages)
        except Exception as e:
            raise RuntimeError(f"Failed to save messages to storage: {e}")
