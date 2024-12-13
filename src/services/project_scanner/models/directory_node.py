from dataclasses import dataclass
from typing import List

from src import FileNode


@dataclass
class DirectoryNode:
    """
    Модель для представления директории.

    Attributes:
        name (str): Имя директории.
        path (str): Абсолютный путь к директории.
        files (List[FileNode]): Список файлов в директории.
        directories (List["DirectoryNode"]): Список поддиректорий.
    """
    name: str
    path: str
    files: List[FileNode]
    directories: List["DirectoryNode"]