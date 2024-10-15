import os
import streamlit as st
import requests

# Get the FastAPI endpoint from an environment variable
FASTAPI_ENDPOINT = os.getenv('FASTAPI_ENDPOINT', 'http://localhost:8000/api')

st.title("Search App")

query = st.text_input("Enter your search query")

if st.button("Search"):
    if query:
        try:
            response = requests.post(f"{FASTAPI_ENDPOINT}/search", json={"query": query})
            if response.status_code == 200:
                st.success("Search Results:")
                st.json(response.json())
            else:
                st.error(f"Error: {response.status_code}")
        except requests.RequestException as e:
            st.error(f"Error connecting to the API: {str(e)}")
    else:
        st.warning("Please enter a search query")

# Display the current FastAPI endpoint (useful for debugging)
st.sidebar.text(f"FastAPI Endpoint: {FASTAPI_ENDPOINT}")