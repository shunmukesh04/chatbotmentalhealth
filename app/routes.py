from flask import Blueprint, request, jsonify, render_template
from .chatbot import get_chatbot_response

routes = Blueprint("routes", __name__)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/chat', methods=['POST'])
def chat():
    try:
        user_query = request.json.get('query')
        if not user_query:
            return jsonify({'response': "I didn't understand that. Please rephrase."}), 400
        
        response = get_chatbot_response(user_query)
        return jsonify({'response': response})

    except Exception as e:
        print(f"🔥 API Error: {e}")  
        return jsonify({'response': "I'm experiencing technical difficulties. Please try again later."}), 500
