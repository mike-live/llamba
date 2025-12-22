from qdrant_client import QdrantClient

class DocumentRepoQdrant():
    def __init__(self, url: str, port: str, collection_name: str, **kwargs):
        self.qdrant_client = QdrantClient(host=url, port=port)
        self.collection_name = collection_name
        self.payload_return = kwargs.get("payload_return", "data")
        self.max_results = kwargs.get("max_results", 5)

    def check_connection(self):
        return True if self.qdrant_client.get_collection(self.collection_name) else False

    def search(self, prompt: str):
        results = self.client.query_points(
            query = prompt,
            collection_name=self.collection_name,
            max_results = self.max_results
        )
        result_data = [result.payload[self.payload_return] for result in results]
        return result_data