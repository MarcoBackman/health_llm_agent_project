import chromadb
from chromadb.utils import embedding_functions
from chromadb.errors import IDAlreadyExistsError, NotFoundError

from common.env_data import EnvData

class ChromaDBConnector:
    def __init__(self):
        # Initialize ChromaDB Client using environment configurations
        self.client = chromadb.PersistentClient(
            path="./chroma_db"  # Persistent storage
        )
        # Define the embedding function (pre-trained model)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        # Retrieve or create the collection
        self.collection = self.client.get_or_create_collection(
            name=EnvData.chroma_index_name,
            embedding_function=self.embedding_function
        )

    def add_document(self, doc_id, text, metadata=None):
        """
        Add a document to the ChromaDB collection.
        :param doc_id: str - Unique identifier for the document
        :param text: str - Main text/content to store and embed
        :param metadata: dict, optional - Additional metadata for filtering/searching
        :return: str - Success message
        """
        try:
            self.collection.add(
                documents=[text],
                ids=[doc_id],
                metadatas=[metadata] if metadata else None
            )
            return f"Document with id '{doc_id}' added successfully."
        except IDAlreadyExistsError:
            raise ValueError(f"Document with id '{doc_id}' already exists.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while adding a document: {e}")

    def get_document(self, doc_id):
        """
        Retrieve a document by its unique ID.
        :param doc_id: str - The ID of the document to retrieve
        :return: dict - Document data including text and metadata
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
                raise NotFoundError(f"Document with id '{doc_id}' not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while retrieving a document: {e}")

    def search_documents(self, query_text, n_results=3):
        """
        Search for similar documents using a query text.
        :param query_text: str - The query to match documents with
        :param n_results: int, optional - Number of results to return
        :return: list - Top matching documents with their metadata
        """
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            # Return a formatted response
            return [
                {
                    "id": results['ids'][i],
                    "text": results['documents'][i],
                    "metadata": results['metadatas'][i] if results['metadatas'] else None,
                    "distance": results['distances'][i]
                }
                for i in range(len(results['ids']))
            ]
        except Exception as e:
            raise RuntimeError(f"An error occurred while searching for documents: {e}")

    def update_document(self, doc_id, text=None, metadata=None):
        """
        Update the text and/or metadata of an existing document.
        :param doc_id: str - The ID of the document to update
        :param text: str, optional - New text content
        :param metadata: dict, optional - New metadata
        :return: str - Success message
        """
        try:
            self.collection.update(
                ids=[doc_id],
                documents=[text] if text else None,
                metadatas=[metadata] if metadata else None
            )
            return f"Document with id '{doc_id}' updated successfully."
        except NotFoundError:
            raise ValueError(f"Document with id '{doc_id}' not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while updating a document: {e}")

    def delete_document(self, doc_id):
        """
        Delete a document by its unique ID.
        :param doc_id: str - The ID of the document to delete
        :return: str - Success message
        """
        try:
            self.collection.delete(ids=[doc_id])
            return f"Document with id '{doc_id}' deleted successfully."
        except Exception as e:
            raise RuntimeError(f"An error occurred while deleting a document: {e}")

    def count_documents(self):
        """
        Return the total number of documents in the collection.
        :return: int - Document count
        """
        try:
            return self.collection.count()
        except Exception as e:
            raise RuntimeError(f"An error occurred while counting documents: {e}")