import logging
from typing import Sequence, TypeVar

from src.logs.handlers.elastic import ElasticsearchHandler, get_elastic_client
from src.core.settings import LoggerSettings, ElasticSettings

LevelType = TypeVar("LevelType")


def setup_logger(
    name: str, level: LevelType, *handlers: Sequence[logging.Handler]
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    for handler in handlers:
        if handler not in logger.handlers:
            logger.addHandler(handler)
    return logger


def get_elastic_handler(
    level: LevelType,
    logger_settings: LoggerSettings = LoggerSettings(),
    elastic_settings: ElasticSettings = ElasticSettings(),
) -> logging.Handler:
    formatter = logging.Formatter(logger_settings.formatter)
    elastic_client = get_elastic_client(elastic_settings)

    es_handler = ElasticsearchHandler(elastic_client, elastic_settings.LOG_INDEX)
    es_handler.setFormatter(formatter)
    es_handler.setLevel(level)

    return es_handler


def setup_logger_stream_handler(
    level: LevelType, settings: LoggerSettings = LoggerSettings()
) -> logging.StreamHandler:
    handler = logging.StreamHandler()
    handler.setFormatter(settings.formatter)
    handler.setLevel(level)

    return handler
