import logging
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure CORS (allow requests from your frontend)
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
CORS(app, resources={r"/chat-morehouse": {"origins": cors_origins}})

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load Morehouse paragraphs (using a placeholder in this case)
MOREHOUSE_PARAS = ["This is a placeholder for the Morehouse paragraphs."]

@app.route("/chat-morehouse", methods=["POST"])
def chat_morehouse():
    try:
        # Validate JSON payload
        data = request.get_json()
        if not data or "message" not in data:
            logger.warning("Missing or invalid message in request body")
            return jsonify({"error": "Missing message in request body"}), 
400

        user_message = data["message"]
        logger.info("Received message: %s", user_message)

        # Construct prompt
        context = "\n".join(MOREHOUSE_PARAS)
        prompt = f"Answer the following question based on the More House 
School information provided:\n\n{context}\n\nQuestion: 
{user_message}\n\nAnswer:"

        # Call OpenAI API
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )

        answer = response.choices[0].message.content.strip()
        logger.info("Generated response: %s", answer)
        return jsonify({"response": answer})

    except Exception as e:
        logger.error("Error in /chat-morehouse: %s", e)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)

