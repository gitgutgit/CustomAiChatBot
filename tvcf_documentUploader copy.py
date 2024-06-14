from openai import OpenAI
import toml

with open("api_secrets.toml", "r") as f:
    secrets = toml.load(f)


api_key_secret = secrets["openai"]["api_key"]
client = OpenAI(api_key =api_key_secret)


# set adding files
file1 = "documents/customer_service.pdf"



def vector_store(file):
 

    vector_store_name = "Customer Service_guidelines_new"
    vector_stores = client.beta.vector_stores.list()
    
    existing_vector_store = None
    for store in vector_stores.data:
        if store.name == vector_store_name:
            existing_vector_store = store
            break
    
    if not existing_vector_store:
        # If it does not exist, create a new vector store
        print("create new vector store\n")
        vector_store = client.beta.vector_stores.create(name=vector_store_name)
    else:
        vector_store = existing_vector_store
        print("already exist\n")

    # Ready the files for upload to OpenAI
    file_paths = [file]
    file_streams = [open(path, "rb") for path in file_paths]
    
    # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    # and poll the status of the file batch for completion.
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
    )
    
    # You can print the status and the file counts of the batch to see the result of this operation.
    print(file_batch.status)
    print(file_batch.file_counts)
    return vector_store




# upload the file to the vector store
mystore =vector_store(file1)


# Save the vector_id to the TOML file
secrets["openai"]["vector_id"] = mystore.id

with open("api_secrets.toml", "w") as f:
    toml.dump(secrets, f)

print("vector_id saved to api_secrets.toml")



