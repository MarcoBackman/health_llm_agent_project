import json
import os

import uvicorn
from fastapi import FastAPI

from agent.impl.dietary_advisor_agent import DietaryAdvisorAgent
from agent.impl.sports_advisor_agent import SportsAdvisorAgent
from api.controller import register_all_controllers
from chroma_db.chroma_db_manager import ChromaDBManager

test_data_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data",
    "test_profile.json"
)

user_profile_test_data_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data",
    "user_profile.txt"
)


### Initialize FastAPI App
app = FastAPI(
    title="ChromaDB + FastAPI RAG Example",
    description="An API for adding documents and querying them with ChromaDB."
)

register_all_controllers(app)


def chunk_text(text, chunk_size=500, overlap=50):
    """
    Chunk a long text into smaller pieces with a specified chunk size and overlap.

    :param text: str - The input text to be chunked.
    :param chunk_size: int - Maximum size of each chunk (in characters).
    :param overlap: int - Number of overlapping characters between chunks.
    :return: list[str] - List of chunks.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end].strip())
        if end >= text_length:
            break
        start = end - overlap
        print(f"start: {start}, end: {end}")

    return chunks


def initialize_user_profile_rag():
    """
    Load user profile data from a text file, chunk it for RAG processing, and store in ChromaDB.

    :param user_profile_path: str - Path to the user profile text file.
    :param chroma_db_manager: ChromaDBManager - Instance of ChromaDBManager for managing storage.
    """
    # Read user profile text
    print(f"Loading user profile data from {user_profile_test_data_path}")
    try:
        with open(user_profile_test_data_path, "r", encoding="utf-8") as file:
            user_profile_text = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found at the path: {user_profile_test_data_path}")

    # Chunk the text for RAG
    chunks = chunk_text(user_profile_text, chunk_size=500, overlap=50)

    print(f"Chunking user profile data: {chunks}")
    # Store chunks in ChromaDB
    for i, chunk in enumerate(chunks):
        doc_id = f"user_profile_chunk_{i+1}"  # Unique ID for each chunk
        metadata = {
            "chunk_index": i + 1,
            "total_chunks": len(chunks),
            "category": "user_profile"
        }

        # Add document to ChromaDB
        result = ChromaDBManager().add_document(doc_id=doc_id, text=chunk, metadata=metadata)
        print(f"Added chunked document: {doc_id}, Result: {result}")

    print("User profile data loaded successfully!")


def initialize_test_data():
    with open(test_data_path, "r") as file:
        test_data = json.load(file)

    # Flatten the test data into a single string for embedding
    document_content = json.dumps(test_data, indent=2)

    # Create a unique doc_id (you can use patient_id or another unique key from the JSON data)
    doc_id = test_data.get("patient_id", "test_profile_default")

    # Optional: Add specific metadata for filtering/searching (e.g., patient info, tags)
    metadata = {
        "name": test_data["profile"]["name"],
        "age": test_data["profile"]["age"],
        "category": "test_data"
    }

    # Initialize ChromaDB Manager
    chroma_db_manager = ChromaDBManager()

    # Add the document into ChromaDB
    result = chroma_db_manager.add_document(
        doc_id=doc_id,
        text=document_content,
        metadata=metadata
    )

    print(f"Test data added to ChromaDB: {result}")

### 4. 어플리케이션 초기화
def initialize_app():
    print(f"어플리케이션 초기화 시작.")
    #ChromaDB 초기화
    ChromaDBManager()
    
    #사전 준비된 데이터 Embedding 후 DB 저장
    initialize_test_data()
    initialize_user_profile_rag()

    #그래프 초기화
    from graph.graph_mananger import GraphManager
    GraphManager.initialize()
    
    #Agent 초기화 및 초기화 확인
    from agent.impl.health_advisor_agent import HealthAdvisorAgent
    DietaryAdvisorAgent()
    HealthAdvisorAgent()
    SportsAdvisorAgent()


### 5. Run the App
if __name__ == "__main__":
    initialize_app()
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")