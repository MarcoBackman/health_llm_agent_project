import os
from langchain.embeddings import HuggingFaceEmbeddings

def get_embedding():
    # logger.info("Embedding 모델 생성", extra=get_log_extra())
    model_name = "jhgan/ko-sbert-nli"
    model_kwargs = {'device': os.environ['DEVICE']}
    encode_kwargs = {'normalize_embeddings': True}

    # This will now use the updated HuggingFaceEmbeddings class
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )