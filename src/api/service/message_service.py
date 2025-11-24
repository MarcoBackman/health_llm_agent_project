from typing import Tuple


from graph.graph_mananger import GraphManager
from graph.state.state import AgentState
from graph.state.state_enum import StateEnum


class MessageService:

    def _check_is_sports_related(self, state: AgentState) -> bool:
        """
        Check if the user's message was determined to be sports-related.

        :param updated_state: The updated state of the graph.
        :return: True if sports-related, False otherwise.
        """
        if not state:
            print("No updated state found. Unable to determine sports-related status.")
            return False

        return state.get("status", False)


    def _form_summary(self, is_sports_related: bool, response: str) -> str:
        """
        Generate a summary for the final response.

        :param is_sports_related: Whether the message is sports-related.
        :param health_advice: Output from the HealthAdvisorAgent.
        :param dietary_advice: Output from the DietaryAgent.
        :return: Summarized string.
        """
        if not is_sports_related:
            return "The message is not related to any sports topic."

        return response

    def process_message(self, user_message) -> Tuple[str, bool]:
        state = {
            "messages": [user_message],
            StateEnum.IS_SPORT_RELATED.value: False,
            "id": "AJ19790515",  # Example values for AgentState TypedDict
            "current_node": StateEnum.START.value,
            "collected_data": {},
            "status": StateEnum.READY,
            "description": "Starting graph execution",
            "tools_used": []
        }

        config = {
            "configurable": {
                "thread_id": "unique_thread_123",
                "checkpoint_ns": "sports_analysis",
                "checkpoint_id": "chkpt_001",
                "dialog_id": "dialog_001"
            }
        }

        print(f"[process_message] Initial State: {state}")
        print(f"[process_message] Invoking Graph: {GraphManager.get_graph()}")

        graph = GraphManager.get_graph()

        try:
            # Step 3: Process the graph to determine if the message is sports-related
            updated_state = graph.invoke(
                state,
                config=config,
            )

            # Step 4: Check if the message is sports-related
            is_sports_related = self._check_is_sports_related(updated_state)

            # Step 5: Retrieve final advisory output if sports-related
            response = updated_state.get("final_response", "No final response found.")

            # Step 6: Generate the summary
            final_message = self._form_summary(is_sports_related, response)
            return final_message, False

        except Exception as e:
            # Handle errors during graph execution
            print(f"An error occurred while processing the message: {str(e)}")
            error_message = f"An error occurred while processing the message: {str(e)}"
            return error_message, True
