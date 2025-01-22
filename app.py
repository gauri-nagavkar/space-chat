import streamlit as st
from agent import Agent

def main():
    # Initialize session state for conversation history
    if "history" not in st.session_state:
        st.session_state["history"] = []

    # Create an agent instance
    agent = Agent().agent

    # Streamlit UI
    st.title("Space Chatbot")
    st.write("Ask me cool things about space, and I'll fetch the data for you!")

    # Display chat history
    for message in st.session_state["history"]:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**Bot:** {message['content']}")

    # Input box for the query
    query = st.text_input("Enter your question:", "")

    if st.button("Ask"):
        if query.strip():
            # Add user query to history
            st.session_state["history"].append({"role": "user", "content": query})

            # Get the response from the agent, including the history as context
            response = agent.chat(query).response

            # Add agent response to history
            st.session_state["history"].append({"role": "assistant", "content": response})

            # Display the updated chat
            st.rerun()  # Updated from st.experimental_rerun()
        else:
            st.write("Please enter a valid query.")

if __name__ == "__main__":
    main()
