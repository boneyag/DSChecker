from dschecker.logging_util.logger import setup_logger
import chromadb
from chromadb.utils import embedding_functions
import os

logger = setup_logger(__name__)


class ChromaDB:
    def __init__(self, collection_name):
        self.client = chromadb.PersistentClient(path=os.path.join(os.path.dirname(__file__), "storage"))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self._embedding_function(),
            metadata={
                "description": "Collection of Python data science code snippets.",
                "hnsw:space": "cosine"
            }
        )

    def _embedding_function(self):
        model = os.path.join(os.path.dirname(__file__), "models/microsoft/codebert-base")
        return embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=model
        )

    def get_num_docs(self):
        return self.collection.count()

    def insert(self, ids, documents, metadatas):
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        logger.info(f"Add documents to the {self.collection.name} collection.")
        logger.info(f"{self.collection.count()} of documents inserted to the {self.collection.name}")

    def search(self, query, n_results=2, condition=None):
        if self.collection.count() == 0:
            logger.info("Empty collection.")
            available_collections = self.client.list_collections()
            if available_collections:
                logger.info("Following collections available")
                for col in available_collections:
                    logger.info(f"Name: {col.name} -- document count: {self.client.get_collection(col.name).count()}")
            return None

        ef = self._embedding_function()
        results = self.collection.query(
            query_embeddings=ef(query),
            where=condition,
            n_results=n_results,
            include=['documents', 'distances', 'metadatas']
        )

        num_results = len(results.get('ids', [[]])[0])
        logger.info(f"Found {num_results}")
        return results
