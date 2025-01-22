import streamlit as st
from agent import Agent

def main():
  # Create an agent instance
  agent = Agent().agent

  # Streamlit UI
  st.title("Space Chatbot")
  st.write("Ask me cool things about space, and I'll fetch the data for you!")

  # Input box for the query
  query = st.text_input("Enter your question:", "")

  if st.button("Ask"):
    if query.strip():
      # Get the response from the agent
      response = agent.chat(query).response
      st.write(response)
    else:
      st.write("Please enter a valid query.")

if __name__ == "__main__":
  main()