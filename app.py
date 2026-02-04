import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from graph import app 

st.set_page_config(page_title="AI Research Assistant", page_icon="🤖")
st.title("LangGraph Wiki Assistant")

with st.sidebar:
    st.header("Settings")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    sys_msg = (
        "You are a helpful assistant. Provide a detailed, comprehensive, and multi-paragraph if the user has not greeted and wants information."
        "Provide with a simple short sentence warm greeting if the user has greeted you."
        "explanation based on the context provided. Use bullet points for key facts and "
        "ensure the response is thorough and easy to read. Do not give one-sentence answers."
    )

    initial_state = {
        "question": prompt,
        "messages": [
            SystemMessage(content=sys_msg),
            HumanMessage(content=prompt)
        ]
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = app.invoke(initial_state)
                response_text = result["response"]
                
                st.markdown(response_text)

                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                st.error(f"Error: {e}")