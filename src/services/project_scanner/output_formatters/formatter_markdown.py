from typing import Union

from src.services.project_scanner.models.directory_node import DirectoryNode
from src.services.project_scanner.models.file_node import FileNode
from src.services.project_scanner.output_formatters.formatter_abstract import FormatterAbstract


class FormatterMarkdown(FormatterAbstract):
    """
    Formats the directory structure into a Markdown representation.
    """

    def format(self, directory_node: DirectoryNode) -> str:
        """
        Formats a DirectoryNode into a Markdown string.

        Args:
            directory_node (DirectoryNode): The directory structure to format.

        Returns:
            str: The Markdown representation of the directory structure.
        """
        lines = []

        def traverse(node: Union[DirectoryNode, FileNode], level: int = 0):
            if isinstance(node, DirectoryNode):
                lines.append(f"{'#' * (level + 1)} {node.name}")
                for subdirectory in node.directories:
                    traverse(subdirectory, level + 1)
                for file in node.files:
                    traverse(file, level + 1)
            elif isinstance(node, FileNode):
                lines.append(f"**{node.name}**\n\n```{node.content}\n```\n")

        traverse(directory_node)
        return "\n".join(lines)
