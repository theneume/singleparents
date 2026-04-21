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

# ─── Client initialised lazily so Render can start without crashing ───────────
_client = None

def get_client():
    global _client
    if _client is None:
        # This setup allows the Cloud API Key to access Vertex features
        # without needing a Service Account file.
        _client = genai.Client(
            api_key=os.environ.get("GOOGLE_API_KEY"),
            http_options=types.HttpOptions(api_version="v1")
        )
        print(f"✓ Gemini client initialized with Cloud API Key + Vertex v1 API")
    return _client


def get_model_name():
    # Use the full Vertex resource path for the model
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")
    return f"projects/{project}/locations/{location}/publishers/google/models/gemini-1.5-flash"


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
    """Handle chat requests with Gemini AI and optional Google Search grounding"""
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
- For event queries, use Google Search to find CURRENT, SPECIFIC events with times and locations
- Always acknowledge the current date ({current_date}) when discussing events or time-sensitive topics
- Format your response with clear sections and bullet points where appropriate
- Be conversational, warm, and personal - avoid generic phrases like "Hello there"
- Ask thoughtful follow-up questions to better understand their situation
- Show empathy and understanding for their challenges

CURRENT USER MESSAGE: {user_message}

Please provide a helpful, personal, and empathetic response."""

        # Detect if we need Google Search (for events/current info)
        needs_search = any(keyword in user_message.lower() for keyword in [
            'event', 'happening', 'this weekend', 'today', 'tomorrow', 'next week',
            'activities', "what's on", 'current', 'latest', 'recent', 'now',
            'schedule', 'upcoming', 'calendar', 'when', 'where can i',
            'things to do', 'places to go', 'fun'
        ])

        # Build generation config
        config = types.GenerateContentConfig(
            temperature=0.8,
            top_k=40,
            top_p=0.95,
            max_output_tokens=2048
        )

        # Google Search grounding works in Vertex AI mode only
        use_vertex = os.environ.get('GOOGLE_GENAI_USE_VERTEXAI', '').lower() == 'true'
        if needs_search and use_vertex:
            config.tools = [types.Tool(google_search=types.GoogleSearch())]

        client = get_client()
        response = client.models.generate_content(
            model=get_model_name(),
            contents=context,
            config=config
        )

        return jsonify({
            'response': response.text,
            'has_grounding': needs_search
        })

    except Exception as e:
        print(f"Error in vertex_chat: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ─── Health check ─────────────────────────────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def health_check():
    use_vertex = os.environ.get('GOOGLE_GENAI_USE_VERTEXAI', '').lower() == 'true'
    api_key_set = bool(
        os.environ.get('GOOGLE_API_KEY') or
        os.environ.get('GEMINI_API_KEY') or
        (use_vertex and os.environ.get('GOOGLE_CLOUD_PROJECT'))
    )
    mode = 'vertex_ai' if use_vertex else 'api_key'
    return jsonify({
        'status': 'ok',
        'api_key_configured': api_key_set,
        'mode': mode,
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8052))
    print(f"\n🚀 Starting Gemini AI server on port {port}")
    print(f"📍 Access at: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)