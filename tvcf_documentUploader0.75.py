import streamlit as st
import toml
from openai import OpenAI

# Load API key from secrets file
with open("api_secrets.toml", "r") as f:
    secrets = toml.load(f)

api_key_secret = secrets["openai"]["api_key"]
client = OpenAI(api_key=api_key_secret)

# Function to list existing vector stores
def list_vector_stores():
    vector_stores = client.beta.vector_stores.list()
    return vector_stores.data

# Function to create a new vector store
def create_vector_store(vector_store_name):
    return client.beta.vector_stores.create(name=vector_store_name)

# Function to upload a file to a vector store
def upload_file_to_vector_store(vector_store_id, file):
    file_streams = [file]
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id, files=file_streams
    )
    return file_batch

# Streamlit UI
st.title("Vector Store Manager")

# Section to create or select a vector store
st.header("Select or Create Vector Store")
vector_store_name_input = st.text_input("Enter vector store name")

vector_stores = list_vector_stores()
vector_store_names = [store.name for store in vector_stores]

selected_vector_store_name = st.selectbox("Select existing vector store", [""] + vector_store_names)

if st.button("Create Vector Store"):
    if vector_store_name_input:
        new_vector_store = create_vector_store(vector_store_name_input)
        st.success(f"Vector store '{vector_store_name_input}' created with ID: {new_vector_store.id}")
    else:
        st.error("Please enter a name for the new vector store")

# Section to upload a file to the selected vector store
st.header("Upload File to Vector Store")
uploaded_file = st.file_uploader("Choose a file")

if st.button("Upload File"):
    if selected_vector_store_name and uploaded_file:
        selected_vector_store = next(store for store in vector_stores if store.name == selected_vector_store_name)
        file_batch = upload_file_to_vector_store(selected_vector_store.id, uploaded_file)
        st.success(f"File uploaded to vector store '{selected_vector_store_name}'. Status: {file_batch.status}")
    else:
        st.error("Please select a vector store and upload a file")

