import os

from langchain_community.vectorstores import Chroma

from commons.path_manager import project_path


# semantic search
def get_vector_store(split_docs, embedding):
    return Chroma.from_documents(split_docs, embedding,
                                 persist_directory=f"{project_path}{os.sep}rag_components{os.sep}vector_stores{os.sep}persist{os.sep}chroma_db")
