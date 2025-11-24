from chroma_db.chroma_db_manager import ChromaDBManager
from tools.llm_api_tool import LlmApiTool


class UserDataRetriever:

    def __init__(self):
        self.db_manager = ChromaDBManager()

    def get_user_profile(self, user_id: str) -> str:
        try:
            document = self.db_manager.get_document(user_id)  # Retrieve user profile by ID
            if not document or "text" not in document:
                print(f"No profile found for user ID: {user_id}")
                return ""
            return document["text"]  # Return the profile text
        except Exception as e:
            print(f"Error retrieving user profile for user ID {user_id}: {str(e)}")
            return ""

    def query_user_profile_rag(self, query, n_results=3):
        # Search for the most relevant chunks in ChromaDB
        try:
            results = ChromaDBManager().search_documents(query_text=query, n_results=n_results)
            print(f"user query data={results}")
        except Exception as e:
            raise RuntimeError(f"Error during ChromaDB search: {e}")

        # If no results are found, return a fallback message
        if not results:
            return "No relevant information found in the user profiles."

        # Extract relevant chunks and their metadata
        top_chunks = [result["text"] for result in results][0]
        if not top_chunks:  # If `top_chunks` is empty after processing
            return "No contextual information available for the query."

        context = "\n\n".join(top_chunks)  # Combine the top chunks for context

        # Prepare the LLM prompt
        augmented_prompt = f"""
        Context:
        {context}

        Question:
        {query}
        """

        # Generate the final response using the LLM
        try:
            final_response = LlmApiTool().send_request(prompt=augmented_prompt)
        except Exception as e:
            raise RuntimeError(f"Error generating response from LLM: {e}")

        return final_response
