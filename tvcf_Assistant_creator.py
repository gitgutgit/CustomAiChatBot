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
        instructions="""당신은 유능한 비서입니다. 제공한 파일에 접근 할 권한이 있으며 대답은 한국어를 사용합니다.
        파일에는 www.tvcf.co.kr 사이트에 고객상담을 진행합니다 현재는 15가지의 가이드라인을 제공하고있습니다. """,
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