from openai import OpenAI
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Initialize Flask app
app = Flask(__name__)
CORS(app)
# Chat endpoint
@app.route('/chat', methods=['POST'])
def chat():
    # Get user message from request
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    # Make a request to OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use any model like GPT-3 or GPT-4
            messages=[
                {"role": "user", "content": user_message}
            ],
            max_tokens=50,
            temperature=0.3
        )
        # Return OpenAI's response
        return jsonify({
            'response': response.choices[0].message.content.strip()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
