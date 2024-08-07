# this only excute once to create assistant or update assistant 
from openai import OpenAI
import toml

with open("api_secrets.toml", "r") as f:
    secrets = toml.load(f)


api_key_secret = secrets["openai"]["api_key"]
mystore_id = secrets["openai"]["vector_id"]
# assistant_id_secret = secrets["openai"]["assistant_id"]

client = OpenAI(api_key =api_key_secret)

def assistant_creator():
    my_assistant = client.beta.assistants.create(
        instructions="""You are a skilled customer support representative for TVCF. You should understand customer inquiries well, find relevant information from the provided files, and deliver the key points concisely in Korean. You have access to the files for customer support on the www.tvcf.co.kr site.

Understand the customer's question, find the appropriate answer in the provided documents, and deliver it in an easy-to-understand and concise manner. Always respond politely and kindly.

응답은 항상 한국어로 해 주세요.
""",
        name="Tvcf customerCenter Assistant",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [mystore_id],}}, #mystore.id 
        model="gpt-4o",
    )
    print(my_assistant)
    return my_assistant.id

# Create the assistant and get its ID
new_assistant_id = assistant_creator()
print("========================================")
# Save the assistant_id to the TOML file
secrets["openai"]["assistant_id"] = new_assistant_id

with open("api_secrets.toml", "w") as f:
    toml.dump(secrets, f)


print("assistant_id saved to api_secrets.toml")