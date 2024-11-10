from flask import Flask, request, jsonify, render_template
from langchain_huggingface import HuggingFaceEndpoint
from langchain.memory import ConversationBufferMemory
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

# Initialize Flask app
app = Flask(__name__)

# Initialize the Hugging Face model using the updated import
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",  # Replace with a more suitable educational model if available
    huggingfacehub_api_token=api_key,
    temperature=0.7
)

# Initialize memory to store chat history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create a prompt template for the educational assistant
prompt_template = """
You are an educational assistant helping a student learn. The student asked:

{input}

Based on the previous conversation:
{chat_history}

Give the best response for the student's learning process:
"""
prompt = PromptTemplate(input_variables=["input", "chat_history"], template=prompt_template)

# Create an LLMChain with memory
educational_chatbot_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory
)

# Serve the HTML file on the root route
@app.route("/")
def index():
    return render_template("index.html")

# Define a route to handle chat messages
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Log the received query for debugging
        print(f"Received query from user: {user_query}")

        # Get response from the LLMChain
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
