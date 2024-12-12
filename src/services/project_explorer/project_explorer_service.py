from typing import Optional, List

from src.services.project_explorer import FileModel
from src.services.project_scanner.filters import AbstractFileFilter, FilterComposite
from src.services.project_explorer.generator_documentation import GeneratorDocumentation
from src.services.project_explorer.generator_project_files import GeneratorProjectFiles
from src.services.project_explorer.generator_project_structure import GeneratorProjectStructure


class ProjectExplorerService:
    """High-level interface for interacting with the project structure and files."""

    def __init__(self, root_directory: str, base_filter: AbstractFileFilter) -> None:
        """
        Initializes the ProjectExplorerService.

        Args:
            root_directory: The root directory of the project.
            base_filter: The base filter applied to all functions.
        """
        self.base_filter = base_filter
        self.generator_project_files = GeneratorProjectFiles(root_directory)
        self.generator_project_structure = GeneratorProjectStructure()
        self.generator_documentation = GeneratorDocumentation(root_directory)

    def _compose_filter(self, additional_filters: Optional[List[AbstractFileFilter]] = None, include_base_filter: bool = True) -> AbstractFileFilter:
        """Composes a filter from the base filter and additional filters."""
        filters = ([self.base_filter] if include_base_filter else []) + (additional_filters or [])
        return FilterComposite(filters)

    def get_structure_as_text(self, relative_path: str, additional_filters: Optional[List[AbstractFileFilter]] = None) -> str:
        """
        Gets the project's structure as a human-readable tree.

        Args:
            relative_path: From where to start search.
            additional_filters: Filters applied on top of the base filter.

        Returns:
            str: Human-readable project structure.
        """
        composite_filter = self._compose_filter(additional_filters)
        return self.generator_project_structure.get_structure_as_text(relative_path, composite_filter)

    def get_project_files(self, relative_path: str, additional_filters: Optional[List[AbstractFileFilter]] = None) -> List[FileModel]:
        """
        Retrieves all files in the project.

        Args:
            relative_path: Directory to start search.
            additional_filters: Filters applied on top of the base filter.

        Returns:
            List[FileModel]: List of project files.
        """
        composite_filter = self._compose_filter(additional_filters)
        return self.generator_project_files.get_file_list(relative_path, composite_filter)

    def get_documentation(self, relative_path: str, additional_filters: Optional[List[AbstractFileFilter]] = None) -> str:
        """
        Generates documentation for the project starting at the given path.

        Args:
            relative_path: Directory to start search.
            additional_filters: Filters applied on top of the base filter.

        Returns:
            str: Markdown-formatted documentation.
        """
        composite_filter = self._compose_filter(additional_filters)
        return self.generator_documentation.get_as_string(relative_path, composite_filter)
