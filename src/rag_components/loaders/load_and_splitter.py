import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, JSONLoader

from commons.logger.logger import LogAgent
from commons.path_manager import PathManager
from langchain.schema import Document

from commons.request_context import get_log_extra


def split_md_by_header(text, delimiter="###"):
    # 헤더 기준으로 split하고 앞에 delimiter를 다시 붙여줌
    parts = text.split(delimiter)
    parts = [f"{delimiter}{p.strip()}" for p in parts if p.strip()]
    return parts

def get_split_docs_with_path(doc_paths):
    all_docs = []

    for doc_path in doc_paths:
        ext = os.path.splitext(doc_path)[-1].lower()

        if ext == ".md":
            # Markdown은 직접 열어서 ### 기준으로 나눔
            with open(doc_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
            split_texts = split_md_by_header(raw_text, delimiter="###")
            for chunk in split_texts:
                all_docs.append(Document(page_content=chunk, metadata={"source": doc_path}))

        elif ext == ".txt":
            loader = TextLoader(doc_path, encoding='utf-8')
            all_docs.extend(loader.load())

        elif ext == ".json":
            # JSONLoader도 정상적으로 추가
            from langchain.document_loaders import JSONLoader
            loader = JSONLoader(file_path=doc_path, jq_schema=".", text_content=False)
            all_docs.extend(loader.load())

        else:
            loader = TextLoader(doc_path, encoding='utf-8')
            all_docs.extend(loader.load())

    # 그 외는 default 청크 처리
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=100)
    return text_splitter.split_documents(all_docs)

    # loaders = []
    # for doc_path in doc_paths:
    #     if doc_path.endswith(".md"):
    #         loaders.append(TextLoader(doc_path, encoding='UTF-8'))
    #     elif doc_path.endswith(".txt"):
    #         loaders.append(TextLoader(doc_path, encoding='UTF-8'))
    #     elif doc_path.endswith(".json"):
    #         JSONLoader(file_path=os.path.join(docs, "aps365_menu.json"), jq_schema=".", text_content=False)
    #     else:
    #         loaders.append(TextLoader(doc_path, encoding='UTF-8'))
    #
    # loaded_docs = []
    # for loader in loaders:
    #     loaded_docs.extend(loader.load_and_split())
    #
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
    # return text_splitter.split_documents(loaded_docs)


def get_split_docs():
    LogAgent.info("Text 로드", extra=get_log_extra())

    jq_schema = """
    .[] | 
    {
      category: .category,
      items: (.subcategories[]? | .subcategories[]? | .subcategories[]? | .items[]?) |
        { 
          name: .name, 
          id: .id, 
          link: .link, 
          table_name: .detail."테이블명", 
          description: .detail."설명" 
        }
    }
    """

    loaders = [
        TextLoader(os.path.join(PathManager.get_doc_path(), "instruction.md"), encoding='UTF-8'),
        TextLoader(os.path.join(PathManager.get_doc_path(), "instruction_for_function.txt"), encoding='UTF-8'),
        TextLoader(os.path.join(PathManager.get_doc_path(), "rule_book.md"), encoding='UTF-8'),
        TextLoader(os.path.join(PathManager.get_doc_path(), "user_manual_of_APS365.md"), encoding='UTF-8'),
        JSONLoader(file_path=os.path.join(PathManager.get_doc_path(), "aps365_menu.json"), jq_schema=jq_schema, text_content=False)
    ]

    loaded_docs = []
    for loader in loaders:
        loaded_docs.extend(loader.load_and_split())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    return text_splitter.split_documents(loaded_docs)
