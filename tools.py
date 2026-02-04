import wikipedia
from langchain_core.tools import tool

@tool
def get_wikipedia_summary(query: str):
    """
    Searches Wikipedia for factual information about a person, place, or concept.
    Returns a short summary.
    """
    try:
        return wikipedia.summary(query, sentences = 50)
    except Exception as e:
        return f"Error searching wikipedia {e}"
    
tools = [get_wikipedia_summary]
def needs_wikipedia(question: str) -> bool:
    q = question.lower()

    triggers = [
        "who is",
        "what is",
        "according to wikipedia",
        "when was",
        "where is",
        "tell me about",
        "explain",
        "biography",
        "history of",
        "What are",
    ]

    return any(t in q for t in triggers)