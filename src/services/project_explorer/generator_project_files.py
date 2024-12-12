import os
from typing import List
from .file_model import FileModel
from src.services.project_scanner.filters import AbstractFileFilter

class GeneratorProjectFiles:
    """Generates a list of files with applied filters."""

    def __init__(self, root_directory: str):
        if not os.path.exists(root_directory):
            raise ValueError(f"Directory '{root_directory}' does not exist.")
        self.root_directory = root_directory

    def get_file_list(self, relative_path: str, composite_filter: AbstractFileFilter) -> List[FileModel]:
        full_path = os.path.join(self.root_directory, relative_path)
        if not os.path.exists(full_path):
            raise ValueError(f"Path '{full_path}' does not exist.")

        file_list = []
        for dirpath, dirnames, filenames in os.walk(full_path):
            dirnames, filenames = composite_filter.filter_files_and_dirs(dirnames, filenames)
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                file_list.append(FileModel(name=filename, path=file_path, content=content))

        return file_list
