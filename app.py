import json
from flask import Flask, request, jsonify, render_template
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load environment variables from the .env file
load_dotenv()

# Get the Hugging Face API key from environment variables
api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Initialize the Hugging Face model using the updated import
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    token=api_key,
    max_length=50,  # Limit the response length to ensure conciseness.
    temperature=0.5  # Lower temperature to make the response more direct and less creative.
)

# Define the JSON file path for storing user information
USER_INFO_FILE = "user_info.json"

# Function to read user information from the JSON file
def read_user_info():
    try:
        with open(USER_INFO_FILE, "r") as file:
            data = json.load(file)
            print(f"DEBUG: Successfully read user info: {data}")
            return data
    except FileNotFoundError:
        print("DEBUG: User info file not found. Returning empty data.")
        return {}
    except json.JSONDecodeError:
        print("DEBUG: JSON decode error occurred. Returning empty data.")
        return {}

# Function to write user information to the JSON file
def write_user_info(data):
    try:
        with open(USER_INFO_FILE, "w") as file:
            json.dump(data, file)
            print(f"DEBUG: Successfully wrote user info: {data}")
    except Exception as e:
        print(f"DEBUG: Error writing to user info file: {str(e)}")

# Create a concise prompt template
prompt_template = """
You are an educational assistant. Keep responses concise and only answer the question directly. Avoid unnecessary elaboration or additional examples.

Student: {input}
Assistant:"""
prompt = PromptTemplate(input_variables=["input"], template=prompt_template)

# Create an LLMChain with simplified memory handling
educational_chatbot_chain = LLMChain(
    llm=llm,
    prompt=prompt
)

# Serve the HTML file on the root route
@app.route("/")
def index():
    return render_template("index.html")

# Define a route to handle chat messages
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_query = data.get("query", "").strip().lower()

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Load existing user information
        user_info = read_user_info()

        # Check if user provides their name
        if "my name is" in user_query:
            # Extract the name from the query
            user_name = user_query.split("my name is")[-1].strip()
            # Store the name in the user_info dictionary and save it to the JSON file
            user_info["user_name"] = user_name
            write_user_info(user_info)
            response = f"Hello {user_name}! Nice to meet you."

        elif "what is my name" in user_query or "do you know my name" in user_query:
            # Retrieve the name from user_info if available
            user_name = user_info.get("user_name", None)
            if user_name:
                response = f"Your name is {user_name}."
            else:
                response = "I'm sorry, I don't have that information. You haven't shared it with me in our conversation yet."

        else:
            # Use the LLMChain to generate a response for general queries
            response = educational_chatbot_chain.predict(input=user_query)

        # Log the generated response for debugging
        print(f"Generated response: {response}")

        return jsonify({"response": response})

    except Exception as e:
        # Log any errors that occur
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": "Something went wrong while processing the request."}), 500

# Run the Flask server
if __name__ == "__main__":
    app.run(port=5000, debug=True)
