"""
Entity definitions for the Hotel Booking Chatbot.

Entities define structured data types that can be extracted from user input.
Each entity has canonical values and their synonyms, following Dialogflow's
entity model.
"""

# ---------------------------------------------------------------------------
# Entity Definitions
# ---------------------------------------------------------------------------
# Format: { entity_name: { canonical_value: [synonym1, synonym2, ...] } }

ENTITIES = {
    "room_type": {
        "Room with AC": [
            "room with ac", "ac room", "air conditioned room", "ac",
            "air conditioned", "airconditioned room", "a/c room"
        ],
        "Cottage": [
            "cottage", "cottage room", "cottages", "cozy cottage"
        ],
        "Villa": [
            "villa", "villa room", "villas", "private villa"
        ],
        "Suite": [
            "suite", "suite room", "suites", "luxury suite", "premium suite"
        ],
        "Deluxe Room": [
            "deluxe room", "deluxe", "deluxe rooms", "dlx room", "dlx"
        ],
        "Standard Room": [
            "standard room", "standard", "normal room", "regular room",
            "basic room", "regular"
        ],
    },

    "guest_count": {
        "Single": ["single", "1 person", "one person", "solo", "1 guest", "one guest"],
        "Double": ["double", "2 persons", "two persons", "couple", "2 guests", "two guests"],
        "Triple": ["triple", "3 persons", "three persons", "3 guests", "three guests"],
        "Family": ["family", "family room", "4 persons", "four persons", "family pack"],
    },
}


def extract_entities(text, entity_name=None):
    """
    Extract entity values from user text.

    Args:
        text (str): The user's input text.
        entity_name (str, optional): Specific entity to extract.
            If None, extracts all entities.

    Returns:
        dict: Mapping of entity_name -> list of matched canonical values.
    """
    text_lower = text.lower().strip()
    results = {}

    entities_to_check = (
        {entity_name: ENTITIES[entity_name]}
        if entity_name and entity_name in ENTITIES
        else ENTITIES
    )

    for ent_name, values in entities_to_check.items():
        matched = []
        for canonical, synonyms in values.items():
            # Sort synonyms by length (longest first) to prefer specific matches
            for synonym in sorted(synonyms, key=len, reverse=True):
                if synonym in text_lower:
                    if canonical not in matched:
                        matched.append(canonical)
                    break  # found a match for this canonical, move on
        if matched:
            results[ent_name] = matched

    return results
