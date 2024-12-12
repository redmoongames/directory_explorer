from typing import Dict, Union, List

from src.services.project_scanner.filters import AbstractFileFilter


class AnalyzerProjectStructure:
    """
    Analyzes the project structure and applies filters to generate a filtered list of files and directories.
    """

    def analyze(self, root_path: str, abstract_filter: AbstractFileFilter) -> Dict[str, Union[List[str], Dict]]:
        """
        Analyze the project structure starting from the root path.

        Args:
            root_path (str): The root directory to analyze.
            abstract_filter (AbstractFileFilter): The filter to apply to files and directories.

        Returns:
            Dict[str, Union[List[str], Dict]]: Filtered structure containing directories and files.
        """
        import os
        structure = {}

        for dirpath, dirnames, filenames in os.walk(root_path):
            filtered_dirs = abstract_filter.filter_dirs(dirnames)
            filtered_files = abstract_filter.filter_files(filenames)

            relative_path = os.path.relpath(dirpath, root_path)
            if relative_path == '.':
                relative_path = root_path

            structure[relative_path] = {
                "directories": filtered_dirs,
                "files": filtered_files
            }

        return structure