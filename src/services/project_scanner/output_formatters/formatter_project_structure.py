from typing import Union

from src.services.project_scanner.models.directory_node import DirectoryNode
from src.services.project_scanner.models.file_node import FileNode
from src.services.project_scanner.output_formatters.formatter_abstract import FormatterAbstract


class FormatterProjectStructure(FormatterAbstract):
    """
    Formats the directory structure into a visually distinctive tree representation.
    """

    def format(self, directory_node: DirectoryNode) -> str:
        """
        Formats a DirectoryNode into a tree structure with visual markers.

        Args:
            directory_node (DirectoryNode): The directory structure to format.

        Returns:
            str: The formatted tree representation of the directory structure.
        """
        lines = []

        def traverse(node: Union[DirectoryNode, FileNode], prefix: str = "", is_last: bool = True):
            connector = "└─ " if is_last else "├─ "
            if isinstance(node, DirectoryNode):
                lines.append(f"{prefix}{connector}{node.name}/")
                # Prepare new prefix for children
                new_prefix = f"{prefix}{'   ' if is_last else '│  '}"
                # Traverse subdirectories and files
                for index, subdirectory in enumerate(node.directories):
                    traverse(subdirectory, new_prefix, index == len(node.directories) - 1 and not node.files)
                for index, file in enumerate(node.files):
                    traverse(file, new_prefix, index == len(node.files) - 1)
            elif isinstance(node, FileNode):
                lines.append(f"{prefix}{connector}{node.name}")

        traverse(directory_node)
        return "\n".join(lines)
