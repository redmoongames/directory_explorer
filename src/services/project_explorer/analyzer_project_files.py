from typing import List

from src.services.project_scanner.filters import AbstractFileFilter


class AnalyzerProjectFiles:
    """
    Extracts and filters files from a given directory.
    """

    def analyze(self, root_path: str, filter: AbstractFileFilter) -> List[str]:
        """
        Analyze and return a filtered list of file paths.

        Args:
            root_path (str): The root directory to analyze.
            filter (AbstractFileFilter): The filter to apply to files.

        Returns:
            List[str]: A list of file paths that match the filter.
        """
        import os
        filtered_files = []

        for dirpath, _, filenames in os.walk(root_path):
            allowed_files = filter.filter_files(filenames)
            filtered_files.extend([os.path.join(dirpath, f) for f in allowed_files])

        return filtered_files