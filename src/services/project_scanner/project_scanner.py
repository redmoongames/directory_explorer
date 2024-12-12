import os
from typing import Optional

from src.services.project_scanner.filters import FilterComposite
from src.services.project_scanner.filters.filter_absract import AbstractFileFilter
from src.services.project_scanner.models.directory_node import DirectoryNode
from src.services.project_scanner.models.file_node import FileNode


class ProjectScanner:
    """
    Scans the project directory and returns its structure as objects with caching support.

    Attributes:
        root_directory (str): The root directory of the project.
        base_filter (AbstractFileFilter): Base filter applied to all scanning operations.
    """

    def __init__(self, root_directory: str, base_filter: AbstractFileFilter) -> None:
        """
        Initializes ProjectScanner.

        Args:
            root_directory (str): The root directory of the project.
            base_filter (AbstractFileFilter): The base filter for filtering files and directories.
        """
        if not os.path.exists(root_directory):
            raise ValueError(f"Directory '{root_directory}' does not exist.")

        self.root_directory = root_directory
        self.base_filter = base_filter

    def fetch_structure(
        self,
        relative_path: str = "./",
        additional_filter: Optional[AbstractFileFilter] = None,
        use_cache: bool = True,
    ) -> DirectoryNode:
        """
        Fetches the project structure as a DirectoryNode object with optional caching.

        Args:
            relative_path (str): Relative path from the root directory to start scanning. Defaults to ".".
            additional_filter (Optional[AbstractFileFilter]): Additional filter to apply on top of the base filter. Defaults to None.
            use_cache (bool): Whether to use cached data if available. Defaults to True.

        Returns:
            DirectoryNode: Object representing the structure of the directory.
        """
        full_path = os.path.join(self.root_directory, relative_path)
        if not os.path.exists(full_path):
            raise ValueError(f"Path '{full_path}' does not exist.")

        # Combine base and additional filters
        composite_filter = self.base_filter
        if additional_filter:
            composite_filter = FilterComposite([self.base_filter, additional_filter])

        structure = self._scan_directory(full_path, composite_filter)

        return structure

    def _scan_directory(self, path: str, file_filter: AbstractFileFilter) -> DirectoryNode:
        """
        Recursively scans a directory and returns its structure as a DirectoryNode.

        Args:
            path (str): The directory path to scan.
            file_filter (AbstractFileFilter): The filter to apply while scanning.

        Returns:
            DirectoryNode: Object representing the directory structure.
        """
        # Normalize the path to ensure consistency
        normalized_path = os.path.normpath(path)

        # Extract directory name for representation
        directory_name = os.path.basename(normalized_path)
        directories = []
        files = []

        # Fetch all directory entries
        entries = list(os.scandir(normalized_path))

        # Separate directories and files
        dir_entries = [entry.path for entry in entries if entry.is_dir()]
        file_entries = [entry.path for entry in entries if entry.is_file()]

        # Apply filters
        allowed_dirs = set(file_filter.filter_dirs(dir_entries))
        allowed_files = set(file_filter.filter_files(file_entries))

        # Process directories
        for dir_path in dir_entries:
            if dir_path in allowed_dirs:
                directories.append(self._scan_directory(dir_path, file_filter))

        # Process files
        for file_path in file_entries:
            if file_path in allowed_files:
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                except PermissionError:
                    content = "<UNREADABLE: PermissionError>"
                except Exception as e:
                    content = f"<UNREADABLE: {e}>"
                files.append(FileNode(name=os.path.basename(file_path), path=file_path, content=content))

        return DirectoryNode(name=directory_name, path=normalized_path, files=files, directories=directories)

    def refresh_cache(self) -> DirectoryNode:
        """
        Forces the cache to refresh with new data by scanning the directory again.

        Returns:
            DirectoryNode: The newly refreshed directory structure.
        """
        return self.fetch_structure(use_cache=False)
