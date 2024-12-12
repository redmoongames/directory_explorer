from dataclasses import dataclass


@dataclass
class FileModel:
    """
    Represents a file in the project with its metadata and content.

    Attributes:
        name (str): The name of the file.
        path (str): The full path to the file.
        content (str): The content of the file as a string.
    """
    name: str
    path: str
    content: str
