import logging
import os

from config.development_config import DevelopmentConfig
from src.services.project_scanner.filters.filter_exclude_directory import FilterExcludeDirectory
from src.services.project_scanner.filters import FilterExcludeFileExtension, FilterComposite
from src.services.project_scanner.filters import FilterExcludeFileName
from src.services.project_scanner.project_overview_service import ProjectOverviewService


def get_config():
    """Выбор конфигурации в зависимости от переменной окружения."""
    env = os.getenv("APP_ENV", "development")

    if env == "development":
        return DevelopmentConfig
    else:
        raise ValueError(f"Unknown environment: {env}")


def main() -> None:

    # Отображаем структуру проекта
    print("-" * 8)
    print("На проекте мы пишем Docstrings документацию на английском языке в формате reStructuredText (reST)")
    print("В функциях мы всегда указываем тип возвращаемого значения. Также везде в проекте мы явно указываем типы")
    print("Проект должен быть написан на уровне Senior программиста с использованием паттернов и архитектурных решений")
    print("Сервисы не должны содержать низкоуровневой логики. Также мы стараемся создавать минимум зависимостей в сервисах")

    project_root = os.path.abspath("./")

    filter_directory = FilterExcludeDirectory(DevelopmentConfig.FILE_FILTERS.ignore_dirs)
    filter_extensions = FilterExcludeFileExtension(DevelopmentConfig.FILE_FILTERS.ignore_extensions)
    filter_files = FilterExcludeFileName(DevelopmentConfig.FILE_FILTERS.ignore_files)
    composite_filter = FilterComposite([filter_directory, filter_extensions, filter_files])

    project_overview_service = ProjectOverviewService(project_root, composite_filter)

    print("=== Project Structure ===")
    structure_tree = project_overview_service.get_project_structure()
    print(structure_tree)

    print("=== Project Documentation ===")
    documentation = project_overview_service.get_project_documentation()
    print(documentation)

    print("=== Project Content ===")
    project_content = project_overview_service.get_project_content("./src/services/project_scanner/")
    print(project_content)

    # Получение и вывод контента файлов внутри папки `src/`
    # print("\n=== Project Content (Markdown Format) ===")
    # project_content = service.get_project_content("src/", additional_filter=additional_filter,
    #                                               formatter=MarkdownFormatter())
    # print(project_content)
    #
    # # Получение и вывод документации проекта в формате JSON
    # print("\n=== Project Documentation ===")
    # project_docs = service.get_project_documentation("src/", additional_filter=additional_filter,
    #                                                  formatter=JSONFormatter())
    # print(project_docs)
    #
    # # Пример обновления кэша
    # print("\nRefreshing cache...")
    # service.refresh_cache()
    # print("Cache refreshed!")


if __name__ == '__main__':
    # Устанавливаем конфигурацию логирования
    logging.basicConfig(
        level=DevelopmentConfig.LOG_LEVEL,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Запуск основного процесса
    main()
