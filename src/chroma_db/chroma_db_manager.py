from chromadb import PersistentClient
from chromadb.errors import IDAlreadyExistsError
from chromadb.utils import embedding_functions
from common.env_data import EnvData

class ChromaDBManager:
    """
        Singleton class for managing the ChromaDB client and collection.
        Ensures that the same instance is reused across the project.
        """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Implement the Singleton pattern to ensure a single instance.
        """
        if not cls._instance:
            cls._instance = super(ChromaDBManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the ChromaDBManager with a persistent ChromaDB client.
        """
        if not hasattr(self, "client"):
            print(f"Chroma DB 초기화 성공")
            # 데이터 기본 저장소 경로
            self.client = PersistentClient(path="./chroma_db")

            # 문장 변환을 위한 임베딩 모델 함수
            self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )

            # Retrieve or create the main collection for managing documents
            self.collection = self.client.get_or_create_collection(
                name=EnvData.chroma_index_name,
                embedding_function=self.embedding_function
            )
            print(f"Chroma DB 초기화 성공")

    def add_document(self, doc_id: str, text: str, metadata: dict = None) -> str:
        """
        Add a document to the ChromaDB collection.

        :param doc_id: str - Unique identifier for the document.
        :param text: str - Document content to store.
        :param metadata: dict, optional - Metadata for the document.
        :return: str - Success message or error.
        """
        try:
            self.collection.add(
                ids=[doc_id],
                documents=[text],
                metadatas=[metadata] if metadata else None
            )
            return f"Document with id '{doc_id}' added successfully."
        except IDAlreadyExistsError:
            return f"Document with id '{doc_id}' already exists."
        except Exception as e:
            raise RuntimeError(f"An error occurred while adding a document: {str(e)}")

    def get_document(self, doc_id: str) -> dict:
        """
        Retrieve a document by its unique ID.

        :param doc_id: str - Unique ID of the document to retrieve.
        :return: dict - Document data including text and metadata.
        """
        try:
            result = self.collection.get(ids=[doc_id])
            if result and result['documents']:
                return {
                    "id": result['ids'][0],
                    "text": result['documents'][0],
                    "metadata": result['metadatas'][0] if result['metadatas'] else None
                }
            else:
                raise ValueError(f"Document with id '{doc_id}' not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while retrieving a document: {str(e)}")

    def search_documents(self, query_text: str, n_results: int = 5) -> list[dict]:
        """
        Search for similar documents using a query text.

        :param query_text: str - Query to match documents with.
        :param n_results: int, optional - Number of top results to return.
        :return: list[dict] - Matching document details with associated metadata.
        """
        try:
            results = self.collection.query(query_texts=[query_text], n_results=n_results)
            return [
                {
                    "id": results['ids'][i],
                    "text": results['documents'][i],
                    "metadata": results['metadatas'][i] if results.get('metadatas') else None,
                    "distance": results['distances'][i]
                }
                for i in range(len(results['ids']))
            ]
        except Exception as e:
            raise RuntimeError(f"An error occurred during document search: {str(e)}")

    def delete_document(self, doc_id: str) -> str:
        """
        Delete a document by its unique ID.

        :param doc_id: str - Unique ID of the document to delete.
        :return: str - Success message or error.
        """
        try:
            self.collection.delete(ids=[doc_id])
            return f"Document with id '{doc_id}' deleted successfully."
        except Exception as e:
            raise RuntimeError(f"An error occurred while deleting the document: {str(e)}")

    def count_documents(self) -> int:
        """
        Return the total number of documents in the collection.

        :return: int - Number of documents in the ChromaDB collection.
        """
        try:
            return self.collection.count()
        except Exception as e:
            raise RuntimeError(f"An error occurred while counting documents: {str(e)}")
