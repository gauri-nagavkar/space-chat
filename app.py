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

    # CSS for chat-like appearance with NASA theme
    st.markdown(
        """
        <style>
        .user-message {
            text-align: right;
            background-color: #1B3A73; /* NASA Blue */
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin: 10px 0;
            display: inline-block;
            max-width: 60%;
        }
        .bot-message {
            text-align: left;
            background-color: #D9D9D6; /* Light Gray */
            color: black;
            padding: 10px;
            border-radius: 10px;
            margin: 10px 0;
            display: inline-block;
            max-width: 60%;
        }
        .chat-container {
            max-width: 700px;
            margin: auto;
        }
        body {
            background-color: #0B0D17; /* Dark Space Gray */
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display chat history with styling
    with st.container():
        for message in st.session_state["history"]:
            if message["role"] == "user":
                st.markdown(
                    f'<div class="chat-container"><div class="user-message">{message["content"]}</div></div>',
                    unsafe_allow_html=True,
                )
            elif message["role"] == "assistant":
                st.markdown(
                    f'<div class="chat-container"><div class="bot-message">{message["content"]}</div></div>',
                    unsafe_allow_html=True,
                )

    # Input box for the query
    query = st.text_input("Enter your question:", "")

    if st.button("Ask"):
        if query.strip():
            # Add user query to history
            st.session_state["history"].append({"role": "user", "content": query})

            # Get the response from the agent
            response = agent.chat(query).response

            # Add agent response to history
            st.session_state["history"].append({"role": "assistant", "content": response})

            # Refresh to show the updated conversation
            st.rerun()
        else:
            st.write("Please enter a valid query.")

if __name__ == "__main__":
    main()
