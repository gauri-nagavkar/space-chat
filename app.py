import streamlit as st
from agent import Agent

def main():
    # Initialize session state for conversation history
    if "history" not in st.session_state:
        st.session_state["history"] = []

    # Create an agent instance
    agent = Agent().agent

    # Streamlit UI
    st.markdown(
        """
        <style>
        .chat-container {
            max-width: 700px;
            margin: auto;
        }
        .user-message {
            text-align: right;
            background-color: #1B3A73; /* NASA Blue */
            color: white;
            padding: 10px;
            border-radius: 15px;
            margin: 10px 0;
            display: inline-block;
            max-width: 60%;
        }
        .bot-message {
            text-align: left;
            background-color: #D9D9D6; /* Light Gray */
            color: black;
            padding: 10px;
            border-radius: 15px;
            margin: 10px 0;
            display: inline-block;
            max-width: 60%;
        }
        body {
            background-color: #0B0D17; /* Dark Space Gray */
            color: white;
        }
        .input-container {
            position: fixed;
            bottom: 0;
            width: 100%;
            padding: 10px;
            background-color: #0B0D17;
            box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.2);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Space Chatbot")
    st.write("Ask me cool things about space, and I'll fetch the data for you!")

    # Display chat history
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

    # Use a local variable for user input
    query = st.text_input("Type your message here...", placeholder="Ask me something about space!")

    # Handle the "Send" button click
    if st.button("Send"):
        if query.strip():
            # Add user query to history
            st.session_state["history"].append({"role": "user", "content": query})

            # Get the response from the agent
            response = agent.chat(query).response

            # Add bot response to history
            st.session_state["history"].append({"role": "assistant", "content": response})

            # Refresh the page to show updated conversation
            st.rerun()
        else:
            st.warning("Please type a message before sending.")

if __name__ == "__main__":
    main()
