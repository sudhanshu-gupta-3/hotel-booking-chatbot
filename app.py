"""
Hotel Booking Chatbot — Flask Application Server.

Serves the web chat interface and handles chat API requests.
Routes:
    GET  /      — Chat UI
    POST /chat  — Process user message and return bot response
"""

from flask import Flask, render_template, request, jsonify
from chatbot import Chatbot

app = Flask(__name__)
bot = Chatbot()


@app.route("/")
def index():
    """Serve the chat UI."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Process a chat message and return the bot's response.

    Expects JSON: {"message": "user text"}
    Returns JSON: {"response", "intent", "entities", "quick_replies"}
    """
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "response": "Please type a message.",
                "intent": None,
                "entities": {},
                "quick_replies": [],
            })

        # Get bot response
        result = bot.get_response(user_message)

        # Determine contextual quick replies based on the matched intent
        quick_replies = _get_quick_replies(result)

        return jsonify({
            "response": result["response"],
            "intent": result["intent"],
            "entities": result["entities"],
            "quick_replies": quick_replies,
        })

    except Exception as e:
        print(f"Error processing message: {e}")
        return jsonify({
            "response": "Sorry, something went wrong. Please try again!",
            "intent": "error",
            "entities": {},
            "quick_replies": ["Book a Room", "Room Types"],
        }), 500


def _get_quick_replies(result):
    """Generate contextual quick-reply suggestions based on the matched intent."""
    intent = result["intent"]
    entities = result.get("entities", {})

    quick_reply_map = {
        "welcome": ["Book a Room", "Room Types", "Check Availability", "Amenities"],
        "room_info": ["Book a Room", "Check Availability", "Pricing"],
        "check_availability": ["Book a Room", "Room Types"],
        "pricing": ["Book a Room", "Check Availability"],
        "booking_confirm": ["Book Another Room", "Room Types", "Goodbye"],
        "booking_cancel": ["Book a Room", "Room Types", "Goodbye"],
        "hotel_amenities": ["Book a Room", "Room Types", "Pricing"],
        "check_in_out": ["Book a Room", "Room Types"],
        "goodbye": [],
        "fallback": ["Book a Room", "Room Types", "Amenities", "Pricing"],
    }

    # Special case: book_room depends on whether entities were extracted
    if intent == "book_room":
        if not entities.get("room_type"):
            return ["Room with AC", "Cottage", "Villa", "Suite", "Deluxe Room"]
        else:
            return ["Confirm", "Cancel"]

    return quick_reply_map.get(intent, ["Book a Room", "Room Types"])


if __name__ == "__main__":
    print("\n[*] Hotel Booking Chatbot is running!")
    print("    Open your browser at: http://localhost:5000\n")
    app.run(debug=True, port=5000)
