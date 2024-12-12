import ast
from typing import Union
from src.services.project_scanner.models.directory_node import DirectoryNode
from src.services.project_scanner.models.file_node import FileNode
from src.services.project_scanner.output_formatters.formatter_abstract import FormatterAbstract


class FileAnalyzer:
    """
    Analyzes Python files to extract information about classes and methods, including their docstrings.
    """

    @staticmethod
    def analyze(file_content: str) -> str:
        """
        Analyzes Python file content to extract classes and methods with their docstrings.

        Args:
            file_content (str): The content of the Python file.

        Returns:
            str: XML-like formatted string containing information about classes and methods.
        """
        try:
            tree = ast.parse(file_content)
        except SyntaxError:
            return "<error>Syntax error in file</error>"

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
                file_code = node.content
                file_analysis = FileAnalyzer.analyze(file_code)
                lines.append("<file>")
                lines.append(f"  <name>{node.name}</name>")
                if file_analysis is not "":
                    lines.append("<doc>")
                    lines.append(file_analysis)
                    lines.append("</doc>")
                lines.append("</file>")
            elif isinstance(node, DirectoryNode):
                # Ignore directories
                for subdirectory in node.directories:
                    traverse(subdirectory)
                for file in node.files:
                    traverse(file)

        traverse(directory_node)
        return "\n".join(lines)
