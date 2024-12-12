from config.base_config import BaseConfig, FileFilters


class DevelopmentConfig(BaseConfig):
    """
    Конфигурация для разработки.
    """

    # Режим отладки включён
    DEBUG_MODE = True

    # Уровень логирования: DEBUG
    LOG_LEVEL = "DEBUG"
