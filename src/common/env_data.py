import os
from dotenv import load_dotenv  # Import the dotenv package
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


class EnvData:

    open_ai_api_key = None
    open_ai_embedding = None
    MAX_TOKEN = 250
    TEMPERATURE = 0.7
    TOP_N = 0.5

    @classmethod
    def load_env_data(cls):
        load_dotenv()

        cls.open_ai_api_key = os.getenv('OPENAI_API_KEY')
        if not cls.open_ai_api_key:
            raise ValueError("Environment variable 'OPENAI_API_KEY' is missing or not set.")

        cls.chroma_server_url = os.getenv('CHROMA_SERVER_URL', 'localhost')
        cls.chroma_server_port = os.getenv('CHROMA_SERVER_PORT', '8010')
        cls.chroma_server_http_protocol = os.getenv('CHROMA_SERVER_HTTP_PROTOCOL', 'http')
        cls.chroma_index_name = os.getenv('CHROMA_INDEX_NAME', 'health_llm_agent_index')
        cls.similarity_threshold: float = float(os.getenv('SIMILARITY_THRESHOLD', 0.3))
        cls.initialize_ai_embedding()
        cls.initialize_open_api()
        cls.check_llm_connection()

    @classmethod
    def initialize_ai_embedding(cls):
        embedding = OpenAIEmbeddings(model="text-embedding-3-small")
        embedding.openai_api_key = cls.open_ai_api_key

        cls.open_ai_embedding = embedding

    @classmethod
    def initialize_open_api(cls):
        cls.llm_tool = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            api_key = cls.open_ai_api_key
        )

    @classmethod
    def check_llm_connection(cls) -> bool:
        """
        Perform a basic test by sending a dummy prompt to verify the LLM connection.
        """
        if cls.llm_tool is None:
            return False

        try:
            # Test connection by sending a minimal valid query
            cls.llm_tool.predict("Hello, LLM!")
            return True
        except Exception as e:
            print(f"LLM Connection Error: {e}")
            return False


#해당 모듈 호출시 데이터 로드
EnvData.load_env_data()