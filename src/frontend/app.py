import streamlit as st
import requests
import json

# Configuration
API_URL = "http://localhost:8000/query"

st.set_page_config(
    page_title="Offer-Pilot Graph Chat",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Offer-Pilot: University Knowledge Graph")
st.markdown("""
Ask questions about universities, courses, and admissions. 
This system retrieves answers directly from the Neo4j Knowledge Graph.
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question (e.g., 'Tell me about Stanford's location')"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            with st.spinner("Searching Knowledge Graph..."):
                response = requests.post(API_URL, json={"query": prompt})
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer received.")
                    full_response = answer
                else:
                    full_response = f"Error: {response.status_code} - {response.text}"
                    
        except requests.exceptions.ConnectionError:
            full_response = "Error: Could not connect to the Backend API. Is it running?"
        except Exception as e:
            full_response = f"An error occurred: {e}"

        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar
with st.sidebar:
    st.header("Status")
    if st.button("Check API Connection"):
        try:
            r = requests.get("http://localhost:8000/health")
            if r.status_code == 200:
                st.success("API is Online")
            else:
                st.error(f"API Returned {r.status_code}")
        except:
            st.error("API is Offline")
    
    st.markdown("---")
    st.markdown("### Sample Questions")
    st.markdown("- Which universities are in the database?")
    st.markdown("- Tell me about Stanford.")
    st.markdown("- Where is Cambridge located?")
