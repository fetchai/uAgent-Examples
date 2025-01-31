# Importing Required libraries
import time

import requests

# Decode the refresh token
token = "Bearer <Your_access_token>"

# Take name of agent from user
name = input("Please give name of your agent? ")
# Create payload for agent creation request
agent_creation_data = {"name": name}
# Post request to create an agent and store address
response_agent = requests.post(
    "https://agentverse.ai/v1/hosting/agents",
    json=agent_creation_data,
    headers={"Authorization": token},
).json()

address = response_agent["address"]
print(f"Agent Address : {address}")

# Reading code to be placed in agent
with open("agent.py", "r") as file:
    code = file.read()
agent_code_data = {"code": code}

# Creating agent.py script for created agent
response_code_update = requests.put(
    f"https://agentverse.ai/v1/hosting/agents/{address}/code",
    json=agent_code_data,
    headers={"Authorization": token},
)

# Starting the agent
requests.post(
    f"https://agentverse.ai/v1/hosting/agents/{address}/start",
    headers={"Authorization": token},
)
time.sleep(10)  # waiting before getting agent's protocol

# Request to get agent protocol digest
response_protcol = requests.get(
    f"https://agentverse.ai/v1/almanac/agents/{address}",
    headers={"Authorization": token},
)
protocol_digest = response_protcol.json()["protocols"][1]
print(f"Protocol Digest : {protocol_digest}")
time.sleep(10)  # Waiting before getting model_digest

# Request to get agent's model details
response_model = requests.get(
    f"https://agentverse.ai/v1/almanac/manifests/protocols/{protocol_digest}",
    headers={"Authorization": token},
)
model = response_model.json()["models"]
time.sleep(10)  # Waiting before storing details to create functions

function_group_ids = requests.get(
    "https://agentverse.ai/v1beta1/function-groups/", headers={"Authorization": token}
)
function_group_id = function_group_ids.json()[0]["uuid"]
time.sleep(10)

# Taking inputs from user for details required to create a function
name_service = input("Please give function name: ")
description = input("Please enter function description: ")
field_name = input("Please enter field name: ")
field_description = input("Please enter field description: ")
tasktype = input("Please tell primary or secondary function: ").upper()

# Logging details provided by user
print(
    f"Service name: {name_service} \nFunction Description: {description} \nField Name: {field_name}\nField Description: {field_description}\nTask Type: {tasktype}"
)

# Storing model digest and name to be used for function creation
model_digest = response_model.json()["interactions"][0]["request"].replace("model:", "")
print(f"Model Digest : {model_digest}")
model_name = model[0]["schema"]["title"]
print(f"Model Name : {model_name}")

# Creating payload for function creation
data = {
    "agent": address,
    "name": name_service,
    "description": description,
    "protocolDigest": protocol_digest,
    "modelDigest": model_digest,
    "modelName": model_name,
    "arguments": [
        {
            "name": field_name,
            "required": True,
            "type": "string",
            "description": field_description,
        }
    ],
    "type": tasktype,
}

# Requesting AI Engine function API to create a function with created payload and storing the response.
response_function = requests.post(
    "https://agentverse.ai/v1beta1/functions/",
    json=data,
    headers={"Authorization": token},
)
# Storing name of function and printing it to check if function was created successfully
name = response_function.json()["name"]
print(f"Function Created with name: {name}")
