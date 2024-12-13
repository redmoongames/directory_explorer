import ast
import json
import logging
from typing import Dict, List, Union

from src import FormatterAbstract, DirectoryNode, FileNode


class FileAnalyzer:
    """
    Analyzes Python files to extract information about classes and methods, including their docstrings.
    """

    @staticmethod
    def analyze(file_content: str) -> List[Dict[str, Union[str, List[Dict[str, str]]]]]:
        """
        Analyzes Python file content to extract classes and methods with their docstrings.

        Args:
            file_content (str): The content of the Python file.

        Returns:
            List[Dict[str, Union[str, List[Dict[str, str]]]]]: A list of dictionaries with class and method information.
        """
        try:
            tree = ast.parse(file_content)
        except SyntaxError as e:
            logging.error(f"Syntax error in file: {e}")
            return [{"error": "Syntax error in file"}]

        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    "class_name": node.name,
                    "class_doc": ast.get_docstring(node) or "No documentation",
                    "methods": []
                }
                for method in [n for n in node.body if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")]:
                    method_info = {
                        "method_name": method.name,
                        "method_doc": ast.get_docstring(method) or "No documentation"
                    }
                    class_info["methods"].append(method_info)
                classes.append(class_info)
        return classes


class FormatterDocumentationJSON(FormatterAbstract):
    """
    Formats the directory structure into a JSON representation with class and method details.
    """

    def format(self, directory_node: DirectoryNode) -> str:
        """
        Formats a DirectoryNode to include files and their class/method documentation in JSON format.

        Args:
            directory_node (DirectoryNode): The directory structure to format.

        Returns:
            str: The JSON-formatted representation of files and their documentation.
        """
        result = []

        def traverse(node: Union[DirectoryNode, FileNode]):
            if isinstance(node, FileNode):
                file_analysis = FileAnalyzer.analyze(node.content)
                result.append({
                    "file_name": node.name,
                    "file_path": node.path,
                    "documentation": file_analysis
                })
            elif isinstance(node, DirectoryNode):
                for subdirectory in node.directories:
                    traverse(subdirectory)
                for file in node.files:
                    traverse(file)

        traverse(directory_node)
        return json.dumps(result, indent=2)


# Example usage:
# Assuming `directory_node` is an instance of DirectoryNode
# formatter = DetailedJSONFormatter()
# print(formatter.format(directory_node))