from typing import Union

from src import FormatterAbstract, DirectoryNode, FileNode


class FormatterProjectStructure(FormatterAbstract):
    """
    Форматтер для представления структуры проекта в виде дерева.
    """

    def format(self, directory_node: DirectoryNode) -> str:
        lines = []

        def file_callback(file: FileNode, prefix: str, is_last: bool):
            connector = "└─ " if is_last else "├─ "
            lines.append(f"{prefix}{connector}{file.name}")

        def directory_callback(directory: DirectoryNode, prefix: str, is_last: bool):
            connector = "└─ " if is_last else "├─ "
            lines.append(f"{prefix}{connector}{directory.name}/")

            # Формируем новый префикс для дочерних элементов
            new_prefix = f"{prefix}{'   ' if is_last else '│  '}"
            for index, subdirectory in enumerate(directory.directories):
                is_last_subdir = index == len(directory.directories) - 1 and not directory.files
                self.traverse_directory(subdirectory, file_callback, directory_callback, new_prefix, is_last_subdir)

            for index, file in enumerate(directory.files):
                is_last_file = index == len(directory.files) - 1
                file_callback(file, new_prefix, is_last_file)

        # Запуск обхода дерева
        directory_callback(directory_node, "", True)

        return "\n".join(lines)

    def traverse_directory(
        self,
        node: Union[DirectoryNode, FileNode],
        file_callback: callable,
        directory_callback: callable,
        prefix: str = "",
        is_last: bool = True,
    ):
        """
        Универсальная функция обхода дерева DirectoryNode.
        Выполняет переданные функции для файлов и директорий.

        Args:
            node (Union[DirectoryNode, FileNode]): Узел дерева.
            file_callback (Callable[[FileNode, str, bool], None]): Функция для обработки файлов.
            directory_callback (Callable[[DirectoryNode, str, bool], None]): Функция для обработки директорий.
            prefix (str): Текущий префикс для форматирования отступов.
            is_last (bool): Указывает, является ли элемент последним в текущей группе.
        """
        if isinstance(node, FileNode):
            file_callback(node, prefix, is_last)
        elif isinstance(node, DirectoryNode):
            directory_callback(node, prefix, is_last)
