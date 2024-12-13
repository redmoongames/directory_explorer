from dataclasses import dataclass
from typing import Optional, List


@dataclass
class FilterSettings:
    ignored_files: Optional[List[str]] = None
    ignored_directories: Optional[List[str]] = None
    ignored_extensions: Optional[List[str]] = None