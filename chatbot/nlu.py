"""
NLU Engine for the Hotel Booking Chatbot.

Uses TF-IDF vectorization and cosine similarity for intent classification,
similar to how Dialogflow's ML engine matches user expressions to intents.
Supports entity extraction, context management, and dynamic response generation.
"""

import re
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .intents import INTENTS
from .entities import extract_entities


class Chatbot:
    """Main chatbot class that handles NLU and response generation."""

    # Minimum similarity score to consider an intent match
    CONFIDENCE_THRESHOLD = 0.3

    # Number of conversation turns a context stays active
    CONTEXT_LIFESPAN = 5

    def __init__(self):
        """Initialize the chatbot by building the TF-IDF model."""
        self.contexts = {}          # {context_name: turns_remaining}
        self.last_intent = None     # Track the last matched intent
        self.last_entities = {}     # Track last extracted entities

        # Build training data for the TF-IDF model
        self._training_phrases = []  # All training phrases (flat list)
        self._phrase_to_intent = []  # Maps each phrase index to its intent

        for intent in INTENTS:
            for phrase in intent["training_phrases"]:
                self._training_phrases.append(self._preprocess(phrase))
                self._phrase_to_intent.append(intent)

        # Build the TF-IDF vectorizer and matrix
        if self._training_phrases:
            self.vectorizer = TfidfVectorizer(
                analyzer="char_wb",   # Character n-grams for better fuzzy matching
                ngram_range=(2, 4),   # Bigrams to 4-grams
                max_features=5000,
            )
            self.tfidf_matrix = self.vectorizer.fit_transform(
                self._training_phrases
            )
        else:
            self.vectorizer = None
            self.tfidf_matrix = None

        # Store the fallback intent for quick access
        self.fallback_intent = next(
            (i for i in INTENTS if i["name"] == "fallback"), INTENTS[-1]
        )

    @staticmethod
    def _preprocess(text):
        """
        Preprocess user input: lowercase, strip, and remove excess whitespace.
        Keeps apostrophes and hyphens for words like "don't" and "check-in".
        """
        text = text.lower().strip()
        # Remove special characters except apostrophes and hyphens
        text = re.sub(r"[^\w\s'\-]", "", text)
        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text)
        return text

    def classify_intent(self, text):
        """
        Classify user text into the best matching intent.

        Uses TF-IDF cosine similarity to find the closest training phrase,
        then checks context requirements (Dialogflow-style input contexts).

        Args:
            text (str): Preprocessed user text.

        Returns:
            dict: The matched intent dictionary.
            float: Confidence score (0.0 - 1.0).
        """
        if not self.vectorizer or not self._training_phrases:
            return self.fallback_intent, 0.0

        # Transform user input
        user_vector = self.vectorizer.transform([text])

        # Compute similarity against all training phrases
        similarities = cosine_similarity(user_vector, self.tfidf_matrix)[0]

        # Get indices sorted by similarity (descending)
        ranked_indices = np.argsort(similarities)[::-1]

        # Try to find a matching intent, respecting context requirements
        for idx in ranked_indices:
            score = similarities[idx]

            # Below threshold — stop looking
            if score < self.CONFIDENCE_THRESHOLD:
                break

            candidate_intent = self._phrase_to_intent[idx]

            # Check context requirement
            required_context = candidate_intent.get("context_required")
            if required_context:
                if required_context not in self.contexts:
                    continue  # Context not active, try next candidate

            return candidate_intent, float(score)

        # No match found — return fallback
        return self.fallback_intent, 0.0

    def get_response(self, user_text):
        """
        Process user input and generate a response.

        This is the main entry point. It:
        1. Preprocesses the text
        2. Classifies the intent
        3. Extracts entities
        4. Generates a response with entity substitution
        5. Manages conversation contexts

        Args:
            user_text (str): Raw user input.

        Returns:
            dict: {
                "intent": intent name,
                "response": bot response text,
                "entities": extracted entities,
                "confidence": match confidence score,
                "context": current active contexts
            }
        """
        processed = self._preprocess(user_text)

        # Classify intent
        intent, confidence = self.classify_intent(processed)

        # Extract entities from the original text (before preprocessing)
        entities = extract_entities(user_text)

        # Merge with last known entities for context continuity
        # (e.g., user says room type, then says "confirm")
        merged_entities = {**self.last_entities}
        merged_entities.update(entities)

        # Select appropriate response
        response = self._build_response(intent, entities, merged_entities)

        # Update contexts
        self._decay_contexts()

        # Set output context if the intent defines one
        if intent.get("context_set"):
            self.contexts[intent["context_set"]] = self.CONTEXT_LIFESPAN

        # Clear contexts on confirm/cancel/goodbye
        if intent["name"] in ("booking_confirm", "booking_cancel", "goodbye"):
            self.contexts.clear()
            self.last_entities.clear()

        # Track state
        self.last_intent = intent["name"]
        if entities:
            self.last_entities.update(entities)

        return {
            "intent": intent["name"],
            "response": response,
            "entities": entities,
            "confidence": round(confidence, 3),
            "context": dict(self.contexts),
        }

    def _build_response(self, intent, entities, merged_entities):
        """
        Build the response string, substituting entity placeholders.

        If an intent expects entities but none were found, use the
        'response_no_entity' variants if available.
        """
        room_types = (
            entities.get("room_type")
            or merged_entities.get("room_type")
            or []
        )

        # Check if intent needs entities but none were found
        has_entity_responses = "response_no_entity" in intent
        if has_entity_responses and not room_types:
            response = random.choice(intent["response_no_entity"])
        else:
            response = random.choice(intent["responses"])

        # Substitute placeholders
        if room_types:
            response = response.replace("{room_type}", room_types[0])
        else:
            # Clean up any remaining placeholders
            response = response.replace("{room_type}", "room")

        return response

    def _decay_contexts(self):
        """
        Decrement all active context lifespans by 1 turn.
        Remove contexts that have expired.
        """
        expired = []
        for ctx_name in self.contexts:
            self.contexts[ctx_name] -= 1
            if self.contexts[ctx_name] <= 0:
                expired.append(ctx_name)

        for ctx_name in expired:
            del self.contexts[ctx_name]
