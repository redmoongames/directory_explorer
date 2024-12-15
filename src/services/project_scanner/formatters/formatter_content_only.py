import ast
import logging
from typing import Union

from .formatter_abstract import FormatterAbstract
from ..models import DirectoryNode, FileNode


class FormatterContent(FormatterAbstract):
    """
    Formatter that outputs only the content of files.

    - Ignores directories.
    - For Python files, removes comments and docstrings from the content.
    - Adds a separator and filename before the content.
    """

    def format(self, directory_node: DirectoryNode) -> str:
        """
        Formats the content of files within the given directory structure.

        Args:
            directory_node (DirectoryNode): The directory structure to format.

        Returns:
            str: The formatted content of the files.
        """
        lines = []

        def traverse(node: Union[DirectoryNode, FileNode]):
            if isinstance(node, FileNode):
                # Add separator and filename
                lines.append(f"<{node.name}>")
                if node.name.endswith(".py"):
                    content = self._process_python_file(node.content)
                else:
                    content = node.content
                lines.append(content)
                lines.append(f"</{node.name}>")

            elif isinstance(node, DirectoryNode):
                # Ignore directories, only process files
                for file in node.files:
                    traverse(file)
                for subdirectory in node.directories:
                    traverse(subdirectory)

        traverse(directory_node)
        return "\n".join(lines)

    def _process_python_file(self, content: str) -> str:
        """
        Processes Python file content to remove comments and docstrings.

        Args:
            content (str): The raw content of the Python file.

        Returns:
            str: The cleaned Python file content.
        """
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            logging.error(f"Syntax error in file: {e}")
            return "<SYNTAX ERROR> Unable to parse Python file."

        cleaned_lines = []

        # Extract original lines for reference
        original_lines = content.splitlines()

        # Track lines used by docstrings
        docstring_lines = set()

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                docstring = ast.get_docstring(node)
                if docstring:
                    # Calculate the start and end lines of the docstring
                    start_line, end_line = node.body[0].lineno - 1, node.body[0].end_lineno
                    docstring_lines.update(range(start_line, end_line))

        for idx, line in enumerate(original_lines):
            stripped = line.strip()
            if idx not in docstring_lines and not stripped.startswith("#"):
                cleaned_lines.append(line)

        return "\n".join(cleaned_lines)

# Example integration in ProjectOverviewService:
# formatter = ContentOnlyFormatter()
# print(formatter.format(directory_node))
