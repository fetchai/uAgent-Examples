# Importing required libraries
import json
import re
import time

import requests

# OAuth and API Configuration
FAUNA_URL = "https://accounts.fetch.ai"
TOKEN_URL = f"{FAUNA_URL}/v1/tokens"
CLIENT_ID = "agentverse"  # Ensure this is your actual Client ID
SCOPE = "av"

# Your encoded refresh token here
refreshed_token = "<YOUR_REFRESH_TOKEN>"
# Decode the refresh token
token = "Bearer <YOUR_ACCESS_TOKEN>"  # Placeholder for initial token


def refresh_tokens(refresh_token):
    """Attempt to refresh the access and refresh tokens."""
    token_response = requests.post(
        TOKEN_URL,
        json={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": CLIENT_ID,
            "scope": SCOPE,
        },
        timeout=10,
    )
    if token_response.status_code == 200:
        print("New token generated.")
        token_response_data = token_response.json()
        return token_response_data["access_token"], token_response_data.get(
            "refresh_token", refresh_token
        )
    print("Error refreshing tokens:", token_response.text)
    return None, None


# Define function to normalize questions asked by AI-engine
def normalize_question(question):
    question_lower = question.lower()
    question_normalized = re.sub(r"[^\w\s]", "", question_lower)
    return question_normalized


# Define function to check if a string is a valid UUID
def is_uuid(key):
    # Ensure the key is a string
    key_str = str(key)
    pattern = re.compile(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-4][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
        re.IGNORECASE,
    )
    return pattern.match(key_str)


# Function to update and refresh the access token
def update_token():
    global token, refreshed_token
    new_tokens = refresh_tokens(refreshed_token)
    fauna_token = new_tokens[0]
    refreshed_token = new_tokens[1]
    token = f"Bearer {fauna_token}"


# Function to handle POST requests with automatic token refresh
def post_request(url, json_data, headers):
    global token
    response = requests.post(url, json=json_data, headers=headers, timeout=10)
    if response.status_code != 200:
        update_token()
        headers["Authorization"] = token
        response = requests.post(url, json=json_data, headers=headers, timeout=10)
    return response


# Function to handle GET requests with automatic token refresh
def get_request(url, headers):
    global token
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        update_token()
        headers["Authorization"] = token
        response = requests.get(url, headers=headers, timeout=10)
    return response


# Functions to interact with the AI-Engine
def send_user_choice_as_uuid(session_id, user_choice, token):
    data = {
        "payload": {
            "type": "user_json",
            "user_json": {"type": "options", "selection": [user_choice]},
            "session_id": session_id,
        }
    }
    return post_request(
        f"https://agentverse.ai/v1beta1/engine/chat/sessions/{session_id}/submit",
        data,
        {"Authorization": token},
    )


def send_user_message(session_id, user_message, token):
    data = {
        "payload": {"type": "user_message", "user_message": user_message},
        "session_id": session_id,
    }
    return post_request(
        f"https://agentverse.ai/v1beta1/engine/chat/sessions/{session_id}/submit",
        data,
        {"Authorization": token},
    )


def stop_session(session_id, token):
    data = {"payload": {"type": "stop"}}
    response = post_request(
        f"https://agentverse.ai/v1beta1/engine/chat/sessions/{session_id}/submit",
        data,
        {"Authorization": token},
    )
    print("Session stopped:", response.json())


# User and model details
data = {"email": "<YOUR_DELTAV_EMAIL_ADDRESS", "requestedModel": "talkative-01"}

response_data = post_request(
    "https://agentverse.ai/v1beta1/engine/chat/sessions", data, {"Authorization": token}
).json()
session_id = response_data.get("session_id")
print("Session Id:", session_id)

# Taking user query as input
objective = input("What Service would you like to assemble?\n")

# Defining initial payload for querying deltaV
data2 = {
    "payload": {
        "type": "start",
        "objective": objective,
        "context": f"User full Name: Test User\nUser email: {data['email']}\nUser location: latitude=51.5072, longitude=0.1276\n",
        "session_id": session_id,
    }
}

response = post_request(
    f"https://agentverse.ai/v1beta1/engine/chat/sessions/{session_id}/submit",
    data2,
    {"Authorization": token},
)
# waiting to get next response from AI engine
time.sleep(10)
response = get_request(
    f"https://agentverse.ai/v1beta1/engine/chat/sessions/{session_id}/responses",
    {"Authorization": token},
).json()

agent_response = response["agent_response"][0]
agent_response_dict = json.loads(agent_response)
# Getting Services options for user's objective
agent_json = agent_response_dict["agent_json"]

# Taking input from user for which service to use.
for option in agent_json["options"]:
    print(f"{option['key']}: {option['value']}")
user_choice = input("Please select an option by entering the corresponding key: \n")

# Payload for selected service
data3 = {
    "payload": {
        "type": "user_json",
        "user_json": {"type": "task_list", "selection": [user_choice]},
    }
}

# Submitting selected service to DeltaV
response = post_request(
    f"https://agentverse.ai/v1beta1/engine/chat/sessions/{session_id}/submit",
    data3,
    {"Authorization": token},
)

# Initialize variables to keep track of the last question and response
last_question = ""
last_response = ""
no_response_count = 0

# Main interaction loop
while True:
    time.sleep(5)
    response = get_request(
        f"https://agentverse.ai/v1beta1/engine/chat/sessions/{session_id}/responses",
        {"Authorization": token},
    )

    if response.status_code != 200:
        raise Exception(
            f"Error in fetching responses: Status code {response.status_code}"
        )

    response = response.json()
    # Handling unresponsive deltaV
    if not response["agent_response"]:
        no_response_count += 1
        print("Waiting for response")
        if no_response_count < 10:
            continue  # Wait for a bit longer if no response yet
        else:
            print("No response from the agent.")
            stop_session(session_id, token)
            break  # Exit loop if no response after several attempts

    no_response_count = 0  # Reset counter on receiving a response

    # Reading agent response
    for agent_resp in response["agent_response"]:
        agent_resp_dict = json.loads(
            agent_resp
        )  # getting response dictionary from deltaV
        current_message_text = ""  # Setting current message to empty string

        if (
            agent_resp_dict.get("type") == "agent_json"
        ):  # handling agent_json type response
            agent_json = agent_resp_dict["agent_json"]
            current_message_text = normalize_question(
                agent_json.get("text", "")
            )  # Setting current message from deltaV

            # Handle options provided in agent_json
            if "options" in agent_json and agent_json["options"]:
                option_keys = [
                    str(option["key"]) for option in agent_json["options"]
                ]  # setting options keys in list to check if its UUID

                # Automatically select the first option if it's a UUID
                if is_uuid(option_keys[0]):
                    print(f"Automatically selecting option: {option_keys[0]}")
                    send_user_choice_as_uuid(session_id, option_keys[0], token)
                    last_response = option_keys[0]  # Update last response
                    continue  # Skip the rest of the loop to wait for the next agent response
                else:
                    # If the first option is not a UUID, prompt for user input
                    print(
                        agent_json.get("text", "")
                    )  # printing deltaV message on terminal
                    for option in agent_json["options"]:
                        print(
                            f"{option['key']}: {option['value']}"
                        )  # Printing options on terminal
                    user_choice = input(
                        "Your Response: "
                    )  # Taking user selection from options
                    send_user_message(
                        session_id, user_choice, token
                    )  # Sending response to deltaV
                    last_response = user_choice  # Update last response
            else:
                # No options provided
                print(
                    agent_json.get(
                        "text",
                        "Please confirm the details or provide the requested information:",
                    )
                )  # Printing user message
                if (
                    agent_json.get("context_json")
                    and "args" in agent_json["context_json"]
                ):  # Printing arguments to confirm if present
                    args = agent_json["context_json"]["args"]
                    for key, value in args.items():
                        print(f"{key}: {value}")
                user_confirmation = input(
                    "Your confirmation/details: "
                )  # Confirming arguments by user
                send_user_message(session_id, user_confirmation, token)
                last_response = user_confirmation  # Update last response

        elif (
            agent_resp_dict.get("type") == "agent_message"
        ):  # handling agent_message type response
            agent_message = agent_resp_dict.get("agent_message", "")
            print(agent_message)
            # If agent_message repeats the last question, reuse last response
            if normalize_question(agent_message.split("?")[0]) == last_question:
                print(f"Reusing your last response: {last_response}")
                send_user_message(session_id, last_response, token)
            else:  # if question not repeated taking input from user
                user_response = input("Your answer: ")
                send_user_message(session_id, user_response, token)
                last_response = user_response  # Update last response

        # Stopping session in case of error.
        elif agent_resp_dict.get("type") == "agent_error":
            agent_message = agent_resp_dict.get("agent_error")
            print(agent_message)
            stop_session(session_id, token)

        elif (
            "agent_info" in agent_resp_dict or agent_resp_dict.get("type") == "stop"
        ):  # handling agent_info and stop messages
            # Print agent_info or handle stop type
            info_message = (
                agent_resp_dict.get("agent_info", "")
                if agent_resp_dict.get("type") == "agent_info"
                else "Session stopping."
            )
            print(f"Agent Info : {info_message}")  # Print agent info
            if (
                "I have completed your task! Please reset your chat session before submitting your new request."
                in info_message
            ):
                stop_session(session_id, token)
                break  # Exit loop if session is stopped
            if agent_resp_dict.get("type") == "stop":
                stop_session(session_id, token)
                break  # Exit loop if session is stopped

        else:
            print(
                "Received an unhandled response type:", agent_resp_dict.get("type")
            )  # Handling any other message type

        # Update last_question with current message text up to a question mark
        last_question = (
            current_message_text.split("?")[0]
            if "?" in current_message_text
            else current_message_text
        )
