"""
Intent definitions for the Hotel Booking Chatbot.

Each intent has:
- name:             Unique identifier
- training_phrases: Example phrases users might say (used for ML matching)
- responses:        Possible bot replies (one is randomly selected)
- entities_used:    Entity types this intent expects
- context_set:      Output context activated when this intent matches
- context_required: Input context that must be active for this intent to match
- action:           Action identifier for the backend to handle
"""

INTENTS = [
    # ------------------------------------------------------------------
    # 1. Welcome / Greeting
    # ------------------------------------------------------------------
    {
        "name": "welcome",
        "training_phrases": [
            "hi", "hello", "hey", "good morning", "good afternoon",
            "good evening", "howdy", "greetings", "hi there",
            "hello there", "hey there", "what's up", "sup",
            "good day", "hola"
        ],
        "responses": [
            "Hello! 👋 Welcome to Grand Hotel. I can help you with room bookings, availability, pricing, and more. How can I assist you today?",
            "Hi there! 🏨 Welcome to Grand Hotel. Would you like to book a room, check availability, or learn about our amenities?",
            "Hey! Welcome to Grand Hotel! 😊 I'm here to help with your stay. What would you like to know?",
            "Good day! Welcome to Grand Hotel. I can assist you with bookings, room info, pricing, and more. How may I help?",
        ],
        "entities_used": [],
        "context_set": None,
        "context_required": None,
        "action": "welcome",
    },

    # ------------------------------------------------------------------
    # 2. Book a Room
    # ------------------------------------------------------------------
    {
        "name": "book_room",
        "training_phrases": [
            "I want to book a room",
            "book a room",
            "reserve a room",
            "I need a room",
            "I'd like to book a room",
            "can I book a room",
            "I want to make a reservation",
            "room booking",
            "book me a room",
            "I want to reserve a villa",
            "book a suite for me",
            "I'd like to reserve a cottage",
            "book a deluxe room",
            "I want an ac room",
            "reserve a standard room please",
        ],
        "responses": [
            "Great choice! 🏨 I'd love to help you book a {room_type}. Shall I go ahead and confirm your reservation?",
            "Wonderful! A {room_type} is an excellent pick. Would you like me to confirm the booking?",
            "Sure! I can book a {room_type} for you right away. Ready to confirm?",
        ],
        "response_no_entity": [
            "I'd be happy to help you book a room! 🛏️ Which type would you prefer?\n\n• Room with AC\n• Cottage\n• Villa\n• Suite\n• Deluxe Room\n• Standard Room",
            "Of course! We have several room types available. Which one interests you?\n\n🏠 Cottage | 🏡 Villa | 🛏️ Suite | ❄️ AC Room | ⭐ Deluxe | 🏨 Standard",
        ],
        "entities_used": ["room_type"],
        "context_set": "booking",
        "context_required": None,
        "action": "initiate_booking",
    },

    # ------------------------------------------------------------------
    # 3. Check Availability
    # ------------------------------------------------------------------
    {
        "name": "check_availability",
        "training_phrases": [
            "is a villa available",
            "check availability",
            "are there any rooms available",
            "do you have rooms",
            "is a suite available",
            "room availability",
            "any rooms free",
            "what rooms are available",
            "is a cottage available",
            "check if deluxe room is available",
            "are rooms open",
        ],
        "responses": [
            "Yes! ✅ Our {room_type} is currently available. Would you like to book it?",
            "Good news! The {room_type} has availability. Shall I reserve one for you?",
        ],
        "response_no_entity": [
            "Let me check for you! 🔍 Which room type are you looking for?\n\n• Room with AC\n• Cottage\n• Villa\n• Suite\n• Deluxe Room\n• Standard Room",
            "I can check availability right away! Which room type would you like me to look up?",
        ],
        "entities_used": ["room_type"],
        "context_set": None,
        "context_required": None,
        "action": "check_availability",
    },

    # ------------------------------------------------------------------
    # 4. Room Info / Room Types
    # ------------------------------------------------------------------
    {
        "name": "room_info",
        "training_phrases": [
            "what rooms do you have",
            "tell me about your rooms",
            "room types",
            "what kind of rooms",
            "show me room options",
            "available room types",
            "list your rooms",
            "describe your rooms",
            "what types of rooms are there",
            "rooms info",
            "room information",
        ],
        "responses": [
            "We have a wonderful selection of rooms! 🏨\n\n❄️ **Room with AC** — Comfortable air-conditioned room\n🏠 **Cottage** — Cozy private cottage with garden view\n🏡 **Villa** — Spacious private villa with premium amenities\n👑 **Suite** — Luxury suite with separate living area\n⭐ **Deluxe Room** — Premium room with enhanced furnishings\n🛏️ **Standard Room** — Clean, comfortable, budget-friendly\n\nWould you like to book any of these?",
            "Here are our room types! 🛏️\n\n1. **Room with AC** — Cool & comfortable\n2. **Cottage** — Private & cozy\n3. **Villa** — Spacious & luxurious\n4. **Suite** — Premium luxury\n5. **Deluxe Room** — Enhanced comfort\n6. **Standard Room** — Great value\n\nWhich one catches your eye?",
        ],
        "entities_used": [],
        "context_set": None,
        "context_required": None,
        "action": "show_rooms",
    },

    # ------------------------------------------------------------------
    # 5. Booking Confirmation (requires 'booking' context)
    # ------------------------------------------------------------------
    {
        "name": "booking_confirm",
        "training_phrases": [
            "yes", "confirm", "book it", "proceed", "go ahead",
            "yes please", "sure", "absolutely", "confirm booking",
            "yes book it", "ok", "okay", "yep", "yeah",
        ],
        "responses": [
            "Your booking is confirmed! ✅🎉 You'll receive a confirmation shortly. Thank you for choosing Grand Hotel!",
            "Excellent! Your reservation is all set! 🎊 We look forward to welcoming you to Grand Hotel!",
            "Done! ✅ Your room has been booked successfully. Thank you for choosing Grand Hotel! Have a wonderful stay!",
        ],
        "entities_used": [],
        "context_set": None,
        "context_required": "booking",
        "action": "confirm_booking",
    },

    # ------------------------------------------------------------------
    # 6. Booking Cancellation (requires 'booking' context)
    # ------------------------------------------------------------------
    {
        "name": "booking_cancel",
        "training_phrases": [
            "no", "cancel", "nevermind", "never mind", "no thanks",
            "don't book", "cancel it", "forget it", "not now",
            "nah", "nope", "no thank you",
        ],
        "responses": [
            "No problem! 😊 The booking has been cancelled. Is there anything else I can help you with?",
            "That's okay! I've cancelled the reservation. Feel free to ask if you need anything else!",
            "Alright, no worries! The booking is cancelled. Let me know if you change your mind! 😊",
        ],
        "entities_used": [],
        "context_set": None,
        "context_required": "booking",
        "action": "cancel_booking",
    },

    # ------------------------------------------------------------------
    # 7. Hotel Amenities
    # ------------------------------------------------------------------
    {
        "name": "hotel_amenities",
        "training_phrases": [
            "what amenities do you have",
            "amenities", "facilities",
            "do you have a swimming pool",
            "is there wifi", "do you have wifi",
            "parking available", "is there parking",
            "gym", "do you have a gym",
            "restaurant", "is there a restaurant",
            "spa", "do you have a spa",
            "what facilities are available",
        ],
        "responses": [
            "Grand Hotel offers these amazing amenities! 🌟\n\n🏊 Swimming Pool\n📶 Free High-Speed WiFi\n🅿️ Free Parking\n🏋️ Fitness Center & Gym\n🍽️ Multi-Cuisine Restaurant\n💆 Luxury Spa & Wellness Center\n🧹 24/7 Housekeeping\n🛎️ Concierge Service\n☕ In-Room Coffee & Tea\n\nWould you like to book a room?",
            "We have plenty to offer! 🏨\n\n🏊 Pool | 📶 WiFi | 🅿️ Parking | 🏋️ Gym\n🍽️ Restaurant | 💆 Spa | 🛎️ Concierge\n☕ Room Service | 🧹 Housekeeping\n\nAnything specific you'd like to know more about?",
        ],
        "entities_used": [],
        "context_set": None,
        "context_required": None,
        "action": "show_amenities",
    },

    # ------------------------------------------------------------------
    # 8. Check-in / Check-out Times
    # ------------------------------------------------------------------
    {
        "name": "check_in_out",
        "training_phrases": [
            "what time is check in",
            "check in time", "checkout time",
            "check out time", "when is check in",
            "when is check out", "what time can I check in",
            "when can I check in", "check-in",
            "check-out", "check in and check out time",
        ],
        "responses": [
            "Here are our check-in/check-out times! 🕐\n\n🟢 **Check-in:** 2:00 PM onwards\n🔴 **Check-out:** By 11:00 AM\n\nEarly check-in and late check-out can be arranged upon request (subject to availability).",
            "⏰ **Check-in** starts at **2:00 PM** and **check-out** is by **11:00 AM**.\n\nNeed early check-in or late check-out? Just let us know!",
        ],
        "entities_used": [],
        "context_set": None,
        "context_required": None,
        "action": "show_timings",
    },

    # ------------------------------------------------------------------
    # 9. Pricing
    # ------------------------------------------------------------------
    {
        "name": "pricing",
        "training_phrases": [
            "how much does a villa cost",
            "room prices", "rates",
            "what are the prices", "pricing",
            "how much for a suite",
            "cost of a room", "room cost",
            "tariff", "room rates",
            "how much is a cottage",
            "price list",
        ],
        "responses": [
            "Here are our room rates per night! 💰\n\n🛏️ **Standard Room** — $80/night\n❄️ **Room with AC** — $100/night\n🏠 **Cottage** — $150/night\n⭐ **Deluxe Room** — $180/night\n👑 **Suite** — $250/night\n🏡 **Villa** — $350/night\n\nPrices may vary based on season and availability. Would you like to book?",
            "Our pricing is very competitive! 💲\n\nStandard: $80 | AC Room: $100 | Cottage: $150\nDeluxe: $180 | Suite: $250 | Villa: $350\n\n*(per night, taxes extra)*\n\nShall I help you make a reservation?",
        ],
        "entities_used": ["room_type"],
        "context_set": None,
        "context_required": None,
        "action": "show_pricing",
    },

    # ------------------------------------------------------------------
    # 10. Goodbye
    # ------------------------------------------------------------------
    {
        "name": "goodbye",
        "training_phrases": [
            "bye", "goodbye", "see you later", "see you",
            "thanks bye", "thank you bye", "good night",
            "take care", "see ya", "cya", "bye bye",
            "thanks and bye", "that's all",
        ],
        "responses": [
            "Goodbye! 👋 Thank you for visiting Grand Hotel. Have a wonderful day!",
            "See you later! 😊 We hope to welcome you at Grand Hotel soon!",
            "Bye bye! 🏨 Thank you for chatting with us. Have a great day!",
            "Take care! 👋 Feel free to come back anytime. We're always here to help!",
        ],
        "entities_used": [],
        "context_set": None,
        "context_required": None,
        "action": "goodbye",
    },

    # ------------------------------------------------------------------
    # 11. Fallback (no training phrases — triggered when nothing matches)
    # ------------------------------------------------------------------
    {
        "name": "fallback",
        "training_phrases": [],
        "responses": [
            "I'm sorry, I didn't quite understand that. 🤔 Could you rephrase? I can help with room bookings, availability, pricing, and more!",
            "Hmm, I'm not sure I follow. Could you try asking in a different way? I'm great at helping with hotel bookings!",
            "I didn't get that. 😅 Here's what I can help with:\n\n• Book a room\n• Check availability\n• Room info & pricing\n• Hotel amenities\n• Check-in/out times",
        ],
        "entities_used": [],
        "context_set": None,
        "context_required": None,
        "action": "fallback",
    },
]
