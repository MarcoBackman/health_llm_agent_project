from langchain_openai import ChatOpenAI

from common.env_data import EnvData

class LlmApiTool:
    """
    Tool to interact with an LLM API for sending queries and receiving responses.
    """

    def __init__(self):
        """
        Initialize the LlmApiTool with necessary configurations.

        :param api_url: Base URL for the LLM API (default: from environment variable).
        :param api_key: API key for authentication (default: from environment variable).
        """
        self.llm_tool: ChatOpenAI = EnvData.llm_tool

    def send_request(self, prompt: str, **kwargs) -> dict:
        """
        Send a request to the LLM tool and return the full response.

        :param prompt: The input query prompt.
        :param kwargs: Additional arguments such as max tokens, temperature, etc.
        :return: A dictionary containing the response from the LLM.
        """
        try:
            response = self.llm_tool.predict(prompt, **kwargs)
            return {"response": response}
        except Exception as e:
            return {"error": str(e)}