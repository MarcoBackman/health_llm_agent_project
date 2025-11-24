import os

from langchain.tools.retriever import create_retriever_tool
# from langgraph.prebuilt import ToolNode

from commons.enums import RagEmbeddings, RagVectorStores, RagRetrievers
from rag_components.loaders.load_and_splitter import get_split_docs_with_path


class RetrieverFactory:
    def __init__(self):
        print(f"###############{('{:^40}'.format('Initializing retriever'))}################")
        self.embedding = self._init_embedding()
        print(f"###############{('{:^40}'.format('Completed setting retriever'))}################")


    def get_retriever(self, doc_paths: list):
        split_docs = get_split_docs_with_path(doc_paths)
        vector_store = self._init_vector_store(split_docs)
        return self._init_retriever(split_docs, vector_store)

    def get_retriever_tool(self, name: str, doc_paths: list, description: str):
        # logger.info(f"Retriever tool 생성: {name}", extra=get_log_extra())
        retriever = self.get_retriever(doc_paths)
        return self._init_retriever_tool(retriever, name, description)

    # def get_retriever_node(self, name: str, doc_paths: list, description: str):
    #     retriever_tool = self.get_retriever_tool(name, doc_paths, description)
    #     return ToolNode([retriever_tool])

    @staticmethod
    def _init_embedding():
        rag_embedder = os.environ[RagEmbeddings.KEY]
        if rag_embedder == RagEmbeddings.KO_SBERT_NLI:
            from rag_components.embeddings.ko_sbert_nli import get_embedding
        elif rag_embedder == RagEmbeddings.BGE_SMALL_EN:
            from rag_components.embeddings.bge import get_embedding
        else:
            from rag_components.embeddings.ko_sbert_nli import get_embedding

        return get_embedding()

    def _init_vector_store(self, split_docs):
        rag_vector_store = os.environ[RagVectorStores.KEY]
        if rag_vector_store == RagVectorStores.FAISS:
            from rag_components.vector_stores.faiss import get_vector_store
        elif rag_vector_store == RagVectorStores.CHROMA:
            from rag_components.vector_stores.chroma import get_vector_store
        else:
            from rag_components.vector_stores.faiss import get_vector_store

        return get_vector_store(split_docs=split_docs, embedding=self.embedding)

    @staticmethod
    def _init_retriever(split_docs, vector_store):
        rag_retriever = os.environ[RagRetrievers.KEY]
        if rag_retriever == RagRetrievers.SEMANTIC_SEARCH:
            from rag_components.retriever.semantic_search_retriever import get_retriever
            return get_retriever(vector_store=vector_store)
        elif rag_retriever == RagRetrievers.DENSE:
            from rag_components.retriever.dense_retriever import get_retriever
            return get_retriever(split_docs=split_docs)
        elif rag_retriever == RagRetrievers.ENSEMBLE:
            from rag_components.retriever.dense_retriever import get_retriever
            dense_retriever = get_retriever(split_docs=split_docs)
            from rag_components.retriever.semantic_search_retriever import get_retriever
            semantic_search_retriever = get_retriever(vector_store=vector_store)
            from rag_components.retriever.ensemble_retriever import get_retriever
            return get_retriever(dense_retriever=dense_retriever, semantic_search_retriever=semantic_search_retriever)
        else:
            from rag_components.retriever.semantic_search_retriever import get_retriever
            return get_retriever(vector_store=vector_store)

    @staticmethod
    def _init_retriever_tool(retriever, name, description):
        # logger.info("retriever Tool 생성", extra=get_log_extra())
        return create_retriever_tool(
            retriever,
            name=name,
            description=description,
        )