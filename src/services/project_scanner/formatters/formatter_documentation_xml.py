import ast
import logging
import traceback
from typing import Union

from .formatter_abstract import FormatterAbstract
from ..models import DirectoryNode, FileNode


class FileAnalyzer:
    """
    Analyzes Python files to extract information about classes and methods, including their docstrings.
    """

    @staticmethod
    def analyze(file_name: str, file_content: str) -> str:
        """
        Analyzes file content to extract classes and methods with their docstrings.

        Args:
            file_name (str): The name of the file.
            file_content (str): The content of the file.

        Returns:
            str: XML-like formatted string containing information about classes and methods
                 or an error message for non-Python files.
        """
        if not file_name.endswith(".py"):
            logging.warning(f"Skipping non-Python file: {file_name}. Check formatter_documentation_xml.py")
            return f"<error>{file_name} is not a Python file and cannot be analyzed.</error>"

        try:
            tree = ast.parse(file_content)
        except SyntaxError as e:
            logging.error(f"Syntax error in file '{file_name}', Exception: {e}\n{traceback.format_exc()}")
            return f"<error>Syntax error in file '{file_name}'</error>"

        lines = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                class_doc = ast.get_docstring(node) or "No documentation"
                lines.append(f"<class>{class_name}</class>")
                lines.append(f"<class_doc>{class_doc}</class_doc>")
                for method in [n for n in node.body if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")]:
                    method_name = method.name
                    method_doc = ast.get_docstring(method) or "No documentation"
                    lines.append(f"<method>{method_name}</method>")
                    lines.append(f"<method_doc>{method_doc}</method_doc>")
        return "\n".join(lines)


class FormatterDocumentationXML(FormatterAbstract):
    """
    Formats the directory structure, focusing on files, their paths, and content details including classes and methods.
    """

    def format(self, directory_node: DirectoryNode) -> str:
        """
        Formats a DirectoryNode to include files, their paths, and detailed class/method information.

        Args:
            directory_node (DirectoryNode): The directory structure to format.

        Returns:
            str: The formatted representation of files and their contents.
        """
        lines = []

        def traverse(node: Union[DirectoryNode, FileNode]):
            if isinstance(node, FileNode):
                file_name = node.name
                file_content = node.content

                file_analysis = FileAnalyzer.analyze(file_name, file_content)

                lines.append("<file>")
                lines.append(f"  <name>{file_name}</name>")
                if file_analysis:
                    lines.append("  <doc>")
                    lines.append(file_analysis)
                    lines.append("  </doc>")
                lines.append("</file>")

            elif isinstance(node, DirectoryNode):
                for subdirectory in node.directories:
                    traverse(subdirectory)
                for file in node.files:
                    traverse(file)

        traverse(directory_node)
        return "\n".join(lines)