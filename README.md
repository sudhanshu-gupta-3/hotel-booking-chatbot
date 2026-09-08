# 🏨 Hotel Booking Chatbot

A Dialogflow-inspired hotel room booking chatbot with NLU (Natural Language Understanding) capabilities, built with Python and Flask.

## ✨ Features

- **Intent Classification** — TF-IDF + Cosine Similarity based ML matching
- **Entity Extraction** — Room types, guest counts with synonym support
- **Context Management** — Multi-turn conversation flow (book → confirm/cancel)
- **Web Chat UI** — Beautiful, responsive chat interface with animations
- **Quick Replies** — Contextual suggestion buttons for guided conversations
- **11 Intents** — Welcome, Book Room, Check Availability, Room Info, Pricing, Amenities, Check-in/out, Confirm, Cancel, Goodbye, Fallback

## 🛠️ Tech Stack

| Layer       | Technology                      |
|-------------|----------------------------------|
| Backend     | Python, Flask                    |
| NLU Engine  | scikit-learn (TF-IDF + Cosine)   |
| Frontend    | HTML5, CSS3, Vanilla JavaScript  |

## 🚀 Setup & Run

### Prerequisites
- Python 3.8 or higher

### Installation

```bash
# 1. Navigate to the project directory
cd ChtBot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the chatbot server
python app.py

# 4. Open in your browser
# Visit: http://localhost:5000
```

## 📁 Project Structure

```
ChtBot/
├── app.py                  # Flask server & API routes
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── chatbot/
│   ├── __init__.py         # Package init
│   ├── nlu.py              # NLU engine (intent classifier + response generator)
│   ├── intents.py          # Intent definitions, training phrases & responses
│   └── entities.py         # Entity definitions with synonym matching
├── templates/
│   └── index.html          # Chat UI page
└── static/
    ├── style.css           # Chat styles
    └── chat.js             # Chat frontend logic
```

## 🧠 How It Works

This chatbot follows **Google Dialogflow's architecture**:

1. **User sends a message** via the web chat UI
2. **Intent Classification**: The NLU engine vectorizes the message using TF-IDF and finds the closest training phrase via cosine similarity
3. **Entity Extraction**: Extracts structured data (room types, etc.) using synonym matching
4. **Context Check**: Verifies required input contexts are active (e.g., "confirm" only works after "book")
5. **Response Generation**: Picks a response template and fills in entity placeholders
6. **Context Update**: Sets output contexts and decays existing ones

## 🔧 Extending the Bot

### Adding a New Intent

Edit `chatbot/intents.py` and add a new dictionary to the `INTENTS` list:

```python
{
    "name": "your_intent_name",
    "training_phrases": ["phrase 1", "phrase 2", ...],
    "responses": ["Response with {entity_placeholder}"],
    "entities_used": ["entity_name"],
    "context_set": None,          # or "context_name"
    "context_required": None,     # or "required_context"
    "action": "your_action",
}
```

### Adding a New Entity

Edit `chatbot/entities.py` and add to the `ENTITIES` dict:

```python
ENTITIES["your_entity"] = {
    "Canonical Value": ["synonym1", "synonym2"],
}
```

## 📚 Based On

This project implements the concepts from [Google Dialogflow](https://cloud.google.com/dialogflow):
- Agents, Intents, Entities, Contexts, Follow-up Intents
- Training Phrases, Actions, Parameters, Responses
- Fulfillment and Webhook patterns

---

*Built as a learning project for conversational AI concepts.*
