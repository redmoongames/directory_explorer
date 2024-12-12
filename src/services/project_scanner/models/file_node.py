from dataclasses import dataclass

@dataclass
class FileNode:
    """
    Модель для представления файла.

    Attributes:
        name (str): Имя файла.
        path (str): Абсолютный путь к файлу.
        content (str): Содержимое файла.
    """
    name: str
    path: str
    content: str
