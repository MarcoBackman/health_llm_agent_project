from langchain_community.vectorstores import FAISS


def get_vector_store(split_docs, embedding):
    # logger.info("vector store 생성: FAISS")
    return FAISS.from_documents(split_docs, embedding)

# pkl_path = f"{path}{os.sep}vector_stores{os.sep}persist{os.sep}faiss_index"
#
# # semantic search
# try:
#     vector_store = FAISS.load_local(folder_path=pkl_path, embeddings=embedding)
# except Exception as e:
#     vector_store = FAISS.from_documents(texts, embedding)
#
# vector_store.save_local(pkl_path)
