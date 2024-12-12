from dataclasses import dataclass


@dataclass
class FileFilters:
    ignore_dirs: list
    ignore_extensions: list
    ignore_files: list


class BaseConfig:
    """
    Общая конфигурация для всех окружений.
    """

    # Корневая директория проекта
    ROOT_DIRECTORY = "./"

    # Фильтры для файлов
    FILE_FILTERS = FileFilters(
        ignore_dirs=["config", "__pycache__", ".venv", ".git", ".idea", ".vscode", ".vscodeproject", "tests"],
        ignore_extensions=[".log", ".tmp"],
        ignore_files=["README.md", ".env", ".DS_Store"]
    )

    # Путь к хранилищу данных (может быть переопределён в наследниках)
    STORAGE_PATH = "./data/storage.json"

    # Логирование
    LOG_LEVEL = "INFO"

    # Флаги для отладки (по умолчанию выключены)
    DEBUG_MODE = False
    ENABLE_PROFILING = False
