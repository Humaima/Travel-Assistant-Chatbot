import streamlit as st
from travel_assistant import TravelAssistant
import time

# Initialize the assistant
if "assistant" not in st.session_state:
    st.session_state.assistant = TravelAssistant()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Set up the page
st.set_page_config(page_title="Travel Assistant", page_icon="✈️")
st.title("✈️ Travel Assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about travel..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Simulate stream of response
        assistant_response = st.session_state.assistant.chat(prompt)
        
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})