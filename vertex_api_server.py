#!/usr/bin/env python3
"""
Vertex AI API Server for Adelaide Single Parents Connect
Handles real-time chat with Google Search grounding
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from google import genai
from google.genai import types
from datetime import datetime

app = Flask(__name__, static_folder='.')
CORS(app)

# ─── Lazy client init ────────────────────────────────────────────────────────
_client = None

def get_client():
    """Get or create the Gemini client."""
    global _client
    if _client is None:
        # Confirming environment integrity
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "single-parents-adelaide")
        location_id = os.environ.get("GOOGLE_CLOUD_LOCATION", "australia-southeast1")

        _client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location_id
        )
        print(f"✓ Client Initialized: Project={project_id} | Region={location_id} | Model=gemini-2.5-flash")
    return _client


def get_model_name():
    """Get the model name - the only model that matters for 2026."""
    return "gemini-2.5-flash"


# ─── Static file serving ──────────────────────────────────────────────────────
@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file(path)


# ─── Chat endpoint ────────────────────────────────────────────────────────────
@app.route('/api/vertex-chat', methods=['POST'])
def vertex_chat():
    """Handle chat requests with Gemini AI"""
    try:
        data = request.json
        user_message = data.get('message', '')
        user_name = data.get('userName')
        conversation_history = data.get('conversationHistory', [])
        relevant_knowledge = data.get('relevantKnowledge', {})

        if not user_message:
            return jsonify({'error': 'Message is required'}), 400

        # Build system context
        current_date = datetime.now().strftime('%A, %B %d, %Y')

        context = f"""You are a warm, empathetic AI assistant for the Adelaide Single Parents Connect platform.

CURRENT DATE: {current_date}
{f"USER'S NAME: {user_name}" if user_name else ""}

YOUR PERSONALITY:
- Warm, caring, and genuinely supportive
- Personal and conversational (use the user's name when you know it)
- Empathetic to the challenges of single parenting
- Professional but friendly
- Encouraging and positive
- Never generic or robotic

"""

        # Add conversation history
        if conversation_history:
            context += "\nCONVERSATION HISTORY:\n"
            for msg in conversation_history:
                context += f"{msg['role'].upper()}: {msg['content']}\n"
            context += "\n"

        # Add relevant knowledge base
        if relevant_knowledge:
            context += "\nRELEVANT KNOWLEDGE BASE:\n"
            context += json.dumps(relevant_knowledge, indent=2)
            context += "\n\n"

        context += f"""IMPORTANT INSTRUCTIONS:
- Use {user_name + "'s" if user_name else "the user's"} name naturally in conversation when appropriate
- Reference previous messages to show you're listening and remembering
- Provide specific contact information (phone numbers, websites) from the knowledge base
- Include clickable links in your response when mentioning websites
- For event queries, help users find CURRENT, SPECIFIC events with times and locations
- Always acknowledge the current date ({current_date}) when discussing events or time-sensitive topics
- Format your response with clear sections and bullet points where appropriate
- Be conversational, warm, and personal - avoid generic phrases like "Hello there"
- Ask thoughtful follow-up questions to better understand their situation
- Show empathy and understanding for their challenges

CURRENT USER MESSAGE: {user_message}

Please provide a helpful, personal, and empathetic response."""

        # Get client and model
        client = get_client()
        model_id = get_model_name()

        # Generate response
        response = client.models.generate_content(
            model=model_id,
            contents=context
        )

        return jsonify({
            'response': response.text,
            'has_grounding': False
        })

    except Exception as e:
        print(f"Error in vertex_chat: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ─── Health check ─────────────────────────────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def health_check():
    api_key_set = bool(os.environ.get('GOOGLE_API_KEY'))
    project_set = bool(os.environ.get('GOOGLE_CLOUD_PROJECT'))
    location_set = bool(os.environ.get('GOOGLE_CLOUD_LOCATION'))
    return jsonify({
        'status': 'ok',
        'api_key_configured': api_key_set,
        'project_configured': project_set,
        'location_configured': location_set,
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8052))
    print(f"\n🚀 Starting Gemini AI server on port {port}")
    print(f"📍 Access at: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)