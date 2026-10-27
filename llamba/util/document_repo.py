import abc

from qdrant_client import QdrantClient



class IDocRepo(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def check_connection(self) -> bool:
        ...

    @abc.abstractmethod
    def search(self, query: str) -> list:
        ...

class DocumentRepoQdrant():
    def __init__(self, url: str, port: str, collection_name: str, **kwargs):
        self.qdrant_client = QdrantClient(host=url, port=port)
        self.collection_name = collection_name
        self.payload_return = kwargs.get("payload_return", "data")
        self.max_results = kwargs.get("max_results", 5)

    def check_connection(self) -> bool:
        return True if self.qdrant_client.get_collection(self.collection_name) else False

    def search(self, prompt: str):
        results = self.client.query_points(
            query = prompt,
            collection_name=self.collection_name,
            max_results = self.max_results
        )
        result_data = [result.payload[self.payload_return] for result in results]
        return result_data


from bio_agents.simple.engine import SearchEngine
from bio_agents.simple import settings as cfg


EngineConnectorSettings = cfg.SearchEngine

class EngineConnector(IDocRepo):
    def __init__(self, search_engine_cfg: cfg.SearchEngine, **kwargs):
        self.settings = search_engine_cfg
        self.search_engine = SearchEngine.from_settings(search_engine_cfg)

    def check_connection(self):
        return self.search_engine.storage.collection_exists()

    def search(self, prompt: str):
        raw_search = self.search_engine.search(prompt)
        text_list = [node.payload['text'] for node in raw_search]
        return text_list