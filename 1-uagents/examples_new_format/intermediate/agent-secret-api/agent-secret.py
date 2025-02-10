# Importing libraries
import requests

# Decode the refresh token
token = "Bearer fauna_access_token"

# Take name of agent and secret details from user
address = input("Please enter address of agent to which you want to add the secret:  ")
name = input("Please enter name for your secret:  ")
secret = input("Please enter value for your secret:  ")

# Create Payload for post request
data = {"address": address, "name": name, "secret": secret}

# Post request to add secret to agent
response_agent = requests.post(
    "https://agentverse.ai/v1/hosting/secrets",
    json=data,
    headers={"Authorization": token},
    timeout=5,
)


# Check if the response code is 200
if response_agent.status_code == 200:
    print("Secret added successfully.")
else:
    print(f"Failed to add secret. Status code: {response_agent.status_code}")
