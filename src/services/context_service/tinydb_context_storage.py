import os
from typing import List, Dict
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from src.services.context_service.context_storage import ContextStorage


class TinyDBContextStorage(ContextStorage):
    """
    TinyDB-based implementation of ContextStorage.

    Provides file-based storage for message contexts using TinyDB with caching for better performance.
    """

    def __init__(self, db_path: str = "data/storage.json"):
        """
        Initializes TinyDBContextStorage with the specified database path.

        Args:
            db_path (str): Path to the JSON file used by TinyDB. Defaults to "data/storage.json".

        Raises:
            ValueError: If the provided db_path is invalid.
        """
        if not db_path.endswith(".json"):
            raise ValueError(f"Invalid database path '{db_path}'. Path must point to a .json file.")
        self._db_path = db_path
        self._db = self._initialize_database()

    def _initialize_database(self) -> TinyDB:
        """
        Ensures the database directory exists and initializes the TinyDB instance with caching.

        Returns:
            TinyDB: An initialized TinyDB instance.
        """
        directory = os.path.dirname(self._db_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        return TinyDB(self._db_path, storage=CachingMiddleware(JSONStorage))

    def save_messages(self, messages: List[Dict[str, str]]) -> None:
        """
        Saves a list of messages to the database.

        Args:
            messages (List[Dict[str, str]]): A list of message dictionaries to save.

        Raises:
            ValueError: If the messages format is invalid.
        """
        if not isinstance(messages, list) or not all(isinstance(msg, dict) for msg in messages):
            raise ValueError("Messages must be a list of dictionaries.")

        self._db.truncate()
        self._db.insert_multiple(messages)

    def load_messages(self) -> List[Dict[str, str]]:
        """
        Loads all messages from the database.

        Returns:
            List[Dict[str, str]]: A list of message dictionaries loaded from the database.
        """
        return self._db.all()

    def close(self) -> None:
        """
        Closes the TinyDB database connection.
        """
        self._db.close()
