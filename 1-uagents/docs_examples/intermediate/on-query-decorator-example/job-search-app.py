import json

from flask import Flask, jsonify, request
from uagents import Model
from uagents.query import query

app = Flask(__name__)

# Define the address of your agent to send requests to
AGENT_ADDRESS = "<YOUR_AGENT_ADDRESS_HERE>"  # Update your agent address here


# Define a data model for incoming requests
class Request(Model):
    query: str


# Define a route to handle job search queries
@app.route("/search-jobs")
async def search_jobs():
    keyword = request.args.get("q")
    if not keyword:
        return jsonify({"error": "No query provided.", "status": "error"}), 400
    # Make a call to the agent with the request and handle the response
    response = await make_agent_call(Request(query=keyword))
    # Check if the response indicates an unsuccessful agent call
    if isinstance(response, str) and response.startswith("Unsuccessful"):
        return jsonify({"error": response, "status": "failed"}), 500

    try:
        # Parse the response to a Python dictionary
        job_data = json.loads(response)
        # Return the job data in a structured format
        return jsonify({"results": job_data, "status": "success"})
    except json.JSONDecodeError:
        # Handle JSON decoding error
        return jsonify({"error": "Invalid response format", "status": "error"}), 500


# Function to send a query to the agent
async def agent_query(req):
    try:
        response = await query(destination=AGENT_ADDRESS, message=req, timeout=15.0)
        # Decode the response and extract data
        data = json.loads(response.decode_payload())
        return data.get("response", "No data found")
    except Exception as e:
        # Return a formatted error message if the agent call fails
        return f"Unsuccessful agent call - {str(e)}"


# Function to initiate an agent call
async def make_agent_call(req: Request):
    response = await agent_query(req)
    return response


# Main function to run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
