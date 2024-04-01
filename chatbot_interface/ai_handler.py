from langchain.langchain_openai import ChatOpenAI
from langchain.langchain_core import messages
from langchain.langgraph import StateGraph, END
from typing import Annotated, TypedDict, Union
import operator
import json

# Assuming API_URL is defined
API_URL = "http://your_api_url_here"


# Define the agent's state, including the operation, the message, and attempts left for processing
class AgentState(TypedDict):
    operation: Annotated[Union[str, None], operator.add]
    message: Annotated[Union[dict, None], operator.add]
    attempts_left: int


# Initialize your LangChain model
model = ChatOpenAI(temperature=0.5, streaming=True)


# Define the function that processes the user's message
async def process_user_message(contents: str, history: list) -> tuple:
    # Define the initial state
    state = AgentState(operation=None, message={}, attempts_left=3)

    # Define your LangGraph
    workflow = StateGraph(schema=AgentState)

    # Define the node to process the message
    async def process_message(state: AgentState) -> AgentState:
        operation, transformed_message = await classify_and_transform(contents, model, history)
        if operation == "NO_COMMAND" and state['attempts_left'] > 0:
            state['attempts_left'] -= 1
            return process_message(state)
        state['operation'] = operation
        state['message'] = transformed_message
        return state

    # Add the process_message node
    workflow.add_node("process_message", process_message)

    # Set the entrypoint
    workflow.set_entry_point("process_message")

    # Set the endpoint
    workflow.add_edge("process_message", END)

    # Compile and run the workflow
    compiled_workflow = workflow.compile()
    final_state = await compiled_workflow.invoke({"messages": [messages.HumanMessage(content=contents)]})

    return (final_state['operation'], final_state['message'])

async def classify_and_transform(contents: str, model: ChatOpenAI, history: list) -> tuple:
    # Example implementation:
    # Use model to classify and transform contents here
    # Return operation and transformed message as a tuple
    return ("ADD", {"name": "Example", "quantity": 1, "price": 9.99})
