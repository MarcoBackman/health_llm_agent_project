import os

from langchain.embeddings import HuggingFaceBgeEmbeddings


def get_embedding():
    model_name = "BAAI/bge-small-en"
    model_kwargs = {'device': os.environ['DEVICE']}
    encode_kwargs = {'normalize_embeddings': True}
    return HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )