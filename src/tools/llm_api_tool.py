from langchain_openai import ChatOpenAI

from common.env_data import EnvData

class LlmApiTool:
    """
    Tool to interact with an LLM API for sending queries and receiving responses.
    """

    def send_request(cls, prompt: str, **kwargs) -> dict:
        """
        Sends a request to the LLM tool and retrieves the response.

        :param prompt: The input query to send to the LLM.
        :param kwargs: Additional keyword arguments like `max_tokens` or `temperature`.
        :return: A dictionary containing the response or an error message.
        """

        try:
            llm_tool = ChatOpenAI()
            response = llm_tool.predict(prompt, **kwargs)
            return {"response": response}
        except Exception as e:
            return {"error": str(e)}


    @classmethod
    def bind_tool_to_api(cls, tools: list):
        """
        model_with_tools

        :param tools:
        :return: returns reponse
        """
        try:
            print("[LlmApiTool] Binding tools with LangChain LLM API...")
            llm_tool: ChatOpenAI = EnvData.llm_tool
            if not cls.llm_tool:
                raise RuntimeError("[LlmApiTool] LLM tool not initialized.")

            # Bind LangChain tools.
            bound_tools = cls.llm_tool.bind_tools(tools)
            print(f"[LlmApiTool] Tools successfully bound: {tools}")
            return bound_tools
        except Exception as e:
            print(f"[LlmApiTool] Failed to bind tools: {str(e)}")
            raise
