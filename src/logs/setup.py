import logging
from typing import Sequence, TypeVar, Optional

from src.logs.handlers.elastic import ElasticsearchHandler, get_elastic_client
from src.core.settings import get_elastic_settings

LevelType = TypeVar("LevelType")


def setup_logger(
    name: str, level: LevelType, handlers: Sequence[logging.Handler]
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    for handler in handlers:
        if handler not in logger.handlers:
            logger.addHandler(handler)
    return logger


def get_elastic_handler(
    format: Optional[str] = "%(asctime)s %(levelname)s %(message)s",
) -> logging.Handler:
    formatter = logging.Formatter(format)
    settings = get_elastic_settings()
    elastic_client = get_elastic_client(settings)

    es_handler = ElasticsearchHandler(elastic_client, settings.LOG_INDEX)
    es_handler.setFormatter(formatter)

    return es_handler
