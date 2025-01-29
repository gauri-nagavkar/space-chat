import streamlit as st
from agent import Agent

# Create an agent
agent = Agent()

# Set up the Streamlit app
st.set_page_config(page_title="Space Chat", page_icon="🚀")

# Load CSS from an external file
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Streamlit app title and description
st.title("🚀 Space Chat")
st.write("Ask me cool things about space, and I'll fetch the data for you!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f'<div class="chat-container"><div class="user-message"><span class="icon">👩🏽‍🚀</span>{message["content"]}</div></div>',
            unsafe_allow_html=True,
        )
    elif message["role"] == "assistant":
        st.markdown(
            f'<div class="chat-container"><div class="bot-message"><span class="icon">🚀</span>{message["content"]}</div></div>',
            unsafe_allow_html=True,
        )

# User input section
query = st.chat_input("Type your message here...", key="chat_input")

if query:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    st.markdown(
        f'<div class="chat-container"><div class="user-message"><span class="icon">👩🏽‍🚀</span>{query}</div></div>',
        unsafe_allow_html=True,
    )

    # Ensure `query` is a valid string before sending to the agent
    if isinstance(query, str) and query.strip():
        # Generate agent response, including conversation history
        response = agent.chat(query, st.session_state.messages).response

        # Add bot response to history
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.markdown(
            f'<div class="chat-container"><div class="bot-message"><span class="icon">🚀</span>{response}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.error("Input must be a valid string. Please try again.")
