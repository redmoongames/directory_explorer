import os
import ast
from typing import List, Dict, Union

from src.services.project_scanner.filters.filter_absract import AbstractFileFilter


class GeneratorDocumentation:
    """
    Generates a concise markdown-formatted documentation summarizing a Python project.
    Filters unnecessary files using a provided FileFilter instance.
    """

    def __init__(self, project_root: str):
        """
        Initializes the documentation generators.

        Args:
            project_root (str): Path to the root directory of the project.
        """
        if not os.path.isdir(project_root):
            raise ValueError(f"Provided path '{project_root}' is not a valid directory.")
        self.project_root = project_root

    def _analyze_file(self, file_path: str) -> Dict[str, Union[str, List[Dict]]]:
        """Analyzes a Python file to extract class and function information."""
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()

        try:
            tree = ast.parse(file_content)
        except SyntaxError:
            return {"file": file_path, "error": "Syntax error"}

        file_info = {"file": file_path, "classes": [], "functions": []}

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "docstring": ast.get_docstring(node) or "MISSING_DOCSTRING",
                    "methods": [
                        {
                            "name": method.name,
                            "docstring": ast.get_docstring(method) or "MISSING_DOCSTRING",
                        }
                        for method in node.body if isinstance(method, ast.FunctionDef)
                    ],
                }
                file_info["classes"].append(class_info)
            elif isinstance(node, ast.FunctionDef):
                func_info = {
                    "name": node.name,
                    "docstring": ast.get_docstring(node) or "MISSING_DOCSTRING",
                }
                file_info["functions"].append(func_info)

        return file_info

    def _generate_markdown(self, analysis: List[Dict]) -> str:
        """Converts the analysis results into a concise markdown string."""
        markdown = ["# Project Overview\n"]

        for file_data in analysis:
            markdown.append(f"## File: {os.path.relpath(file_data['file'], self.project_root)}")
            if "error" in file_data:
                markdown.append(f"**Error:** {file_data['error']}\n")
                continue

            for cls in file_data.get("classes", []):
                markdown.append(f"### Class: {cls['name']}")
                markdown.append(f"- **Docstring:** {cls['docstring']}")
                for method in cls["methods"]:
                    markdown.append(f"  - **Method:** {method['name']} - {method['docstring']}")

            for func in file_data.get("functions", []):
                markdown.append(f"### Function: {func['name']}")
                markdown.append(f"- **Docstring:** {func['docstring']}")

        return "\n".join(markdown)

    def get_as_string(self, path: str, file_filter:  AbstractFileFilter) -> str:
        """
        Generates the markdown documentation for the project starting from a given path.

        Args:
            path (str): The directory path to start generating documentation.

        Returns:
            str: Markdown-formatted summary of the project.
            :param file_filter:
        """
        analysis = []
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if not file_filter.is_file_allowed(file_path):
                    continue
                if file.endswith(".py"):
                    analysis.append(self._analyze_file(file_path))

        return self._generate_markdown(analysis)
