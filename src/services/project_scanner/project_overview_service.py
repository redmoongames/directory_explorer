from typing import List, Optional, Union

from src.services.project_scanner.filters import AbstractFileFilter
from src.services.project_scanner.output_formatters.formatter_abstract import FormatterAbstract
from src.services.project_scanner.output_formatters.formatter_content_only import FormatterContentOnly

from src.services.project_scanner.output_formatters.formatter_documentation_xml import FormatterDocumentationXML
from src.services.project_scanner.output_formatters.formatter_documentation_json import FormatterDocumentationJSON
from src.services.project_scanner.output_formatters.formatter_markdown import FormatterMarkdown
from src.services.project_scanner.output_formatters.formatter_project_structure import FormatterProjectStructure
from src.services.project_scanner.project_scanner import ProjectScanner


class ProjectOverviewService:
    """
    Provides a high-level interface for fetching and formatting project structure and content.

    Attributes:
        project_scanner (ProjectScanner): Handles project scanning operations.
    """

    def __init__(
        self,
        root_directory: str,
        base_filter: AbstractFileFilter,
    ) -> None:
        """
        Initializes the ProjectOverviewService.

        Args:
            root_directory (str): The root directory of the project.
            base_filter (AbstractFileFilter): The base filter for filtering files and directories.
        """
        self.project_scanner = ProjectScanner(root_directory, base_filter)

    def get_project_structure(
        self,
        relative_path: str = ".",
        additional_filter: Optional[AbstractFileFilter] = None,
    ) -> str:
        """
        Fetches and formats the project structure.

        Args:
            relative_path (str): The starting path relative to the root directory. Defaults to ".".
            additional_filter (Optional[AbstractFileFilter]): Additional filters to apply. Defaults to None.

        Returns:
            str: Formatted project structure.
        """
        formatter = FormatterProjectStructure()
        structure = self.project_scanner.fetch_structure(relative_path, additional_filter)
        return formatter.format(structure)

    def get_project_content(
        self,
        relative_path: str = ".",
        additional_filter: Optional[AbstractFileFilter] = None,
    ) -> str:
        """
        Fetches and formats the content of all files in the project.

        Args:
            relative_path (str): The starting path relative to the root directory. Defaults to ".".
            additional_filter (Optional[AbstractFileFilter]): Additional filters to apply. Defaults to None.
            formatter (Optional[FormatterAbstract]): Formatter to use for output. Defaults to MarkdownFormatter.

        Returns:
            str: Formatted project content.
        """
        formatter = FormatterContentOnly()
        structure = self.project_scanner.fetch_structure(relative_path, additional_filter)
        return formatter.format(structure)

    def get_project_documentation(
        self,
        relative_path: str = ".",
        additional_filter: Optional[AbstractFileFilter] = None,
    ) -> str:
        """
        Fetches and formats the project documentation (classes and functions).

        Args:
            relative_path (str): The starting path relative to the root directory. Defaults to ".".
            additional_filter (Optional[AbstractFileFilter]): Additional filters to apply. Defaults to None.
            formatter (Optional[FormatterAbstract]): Formatter to use for output. Defaults to JSONFormatter.

        Returns:
            str: Formatted project documentation.
        """
        # formatter = DocumentationJSONFormatter()
        formatter = FormatterDocumentationXML()
        structure = self.project_scanner.fetch_structure(relative_path, additional_filter)
        return formatter.format(structure)

    def refresh_cache(self) -> None:
        """
        Refreshes the cache of the ProjectScanner.
        """
        self.project_scanner.refresh_cache()

# Example usage:
# service = ProjectOverviewService("/path/to/project", base_filter)
# print(service.get_project_structure())
# print(service.get_project_content("src/"))
# print(service.get_project_documentation(formatter=MarkdownFormatter()))
