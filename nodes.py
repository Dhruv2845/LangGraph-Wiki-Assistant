import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, AIMessage
from state import AgentState
from tools import get_wikipedia_summary, needs_wikipedia

load_dotenv()

client = ChatGroq(
    api_key=os.getenv("API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0
)

def classify(state:AgentState) -> AgentState:
    question = state.question.lower()
    prompt = f"""
    Classify the following user input into exactly one of these categories: 'greetings' or 'search'.
    - 'greetings': If the user is saying hi, hello, or basic pleasantries.
    - 'search': If the user is asking a factual question or seeking information.
    
    Return ONLY the category name.
    
    User input: "{question}"
    """

    classification = client.invoke(prompt).content.strip().lower()

    if "greetings" in classification:
        label = "greetings"
    else:
        label = "search"
    return {
        "classification" : label
    }
def respond_search(state: AgentState) -> AgentState:
    messages = state.messages
    question = state.question

    
    if needs_wikipedia(question):

        wiki_result = get_wikipedia_summary.run(question)

        messages.append(
            SystemMessage(
                content=f"The following information was fetched from Wikipedia:\n{wiki_result}"
            )
        )

        final_response = client.invoke(messages)

        return {
            "messages": [final_response] ,
            "response": final_response.content
        }

    
    response = client.invoke(messages)
    return {
        "messages": messages + [response],
        "response": response.content
    }

def respond_greetings(state:AgentState) -> AgentState:
    """Simple greeting node (no tools needed here)."""
    prompt = f"""
    The user said:'{state.question}'

    INSTRUCTIONS:
    - You are a friendly assistant.
    - Greet the user warmly.
    - Keep your response to exactly one short, friendly sentence.
    - Do answer any qustion if user has asked.
    """
    res = client.invoke(prompt)
    return {
        "messages": [res],
        "response": res.content
    }