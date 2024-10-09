from logging import Handler
from elasticsearch import Elasticsearch
from src.core.settings import ElasticSettings


class ElasticsearchHandler(Handler):
    def __init__(self, es_client: Elasticsearch, index_name: str):
        super().__init__(self)
        self.es_client = es_client
        self.index_name = index_name

    def emit(self, record):
        log_entry = self.format(record)
        self.es_client.index(index=self.index_name, body=log_entry)


def get_elastic_client(settings: ElasticSettings) -> Elasticsearch:
    return Elasticsearch([{"host": settings.HOST, "port": settings.PORT}])
