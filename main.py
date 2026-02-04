from langchain_core.messages import HumanMessage, SystemMessage
from graph import app


def run_bot():
    print("Chat with ai assistant.")
    print("Type your question below, type 'exit' to quit \n")

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.strip().lower() in ["exit", "quit", "q"]:
                print("bot: Goodbye!")
                break

            sys_msg =(
                "You are a helpful assistant. Provide a detailed, comprehensive, and multi-paragraph if the user has not greeted and wants information."
                "Provide with a simple short sentence warm greeting if the user has greeted you."
                "explanation based on the context provided. Use bullet points for key facts and "
                "ensure the response is thorough and easy to read. Do not give one-sentence answers."
            )
            initial_state = {
                "question":user_input,
                "messages": [
                    SystemMessage(content=sys_msg),
                    HumanMessage(content=user_input)
                ]
            }
            # x = needs_wikipedia(initial_state["question"])
            result = app.invoke(initial_state)
            print(f"Bot: {result['messages'][-1].content}")
        
        except Exception as e:
            if "recursion limit" in str(e).lower():
                print("stuck in a loop and stopped to save tokens.")
            elif "rate limit" in str(e).lower():
                print("Quota exceeded. wait or switch models.")
            else:
                print(f"Bot Error: {e}")

if __name__ == "__main__":
    run_bot()