# Chatbot Instructions Summary

Based on the Dialogflow chatbot instructions document.

## 1. Basics

- **Agents**: Virtual agents that handle conversations with end-users. Acts as a natural language understanding module that understands human language nuances. Translates end-user text/audio to structured data.

- **Intents**: Categorize an end-user's intention for one conversation turn. Combined intents can handle a complete conversation. Matching an intent is also known as intent classification.

  - **Training phrases**: Example phrases for what end-users might say. Dialogflow's built-in ML expands on the list with similar phrases.
  - **Action**: Defined for each intent. Provided to your system when an intent is matched.
  - **Parameters**: Extracted values from end-user expression as parameters. Each parameter has a type (entity type).
  - **Responses**: Text, speech, or visual responses returned to the end-user.

- **Entities**: Types for extracting data from end-user expressions.
  - **System entities**: Predefined for common types (dates, times, colors, email addresses).
  - **Developer entities**: Custom entities for matching custom data (e.g., a "vegetable" entity for a grocery store agent).

- **Contexts**: Control conversation flow.
  - **Input contexts**: Must be active for an intent to match.
  - **Output contexts**: Become active when an intent is matched.
  - **Follow-up intents**: Automatically set contexts for pairs of intents. A child of its parent intent. Only matched when the parent intent is matched.

- **Dialogflow Console**: Web UI for creating, building, and testing agents. Different from GCP Console (used for billing and GCP resources).

## 2. User Interactions with Integrations

- Dialogflow integrates with popular platforms: Google Assistant, Slack, Facebook Messenger.
- **Integrations options**: Provide platform-specific features for building rich responses.
- Direct end-user interactions are handled for you, so you can focus on building your agent.

## 3. Fulfillment for Integrations

- If using integrations and the agent needs more than static intent responses, use **fulfillment** to connect your service to the agent.
- **Connecting your service**: Allows taking actions based on end-user expressions and sending dynamic responses.
- **When to enable fulfillment**: If an intent requires some action by your system or a dynamic response.
- **Processing flow**:
  1. End-user types/speaks an expression
  2. Dialogflow matches to an intent and extracts parameters
  3. Dialogflow sends a webhook request message to your webhook service (contains matched intent, action, parameters, response)
  4. Your service performs actions (database queries, external API calls)
  5. Your service sends a webhook response message to Dialogflow (contains response to send to end-user)
  6. Dialogflow sends the response to the end-user
  7. End-user sees/hears the response

## 4. User Interactions with the API

- If not using integration options, must write code that directly interacts with the end-user.
- Must interact with Dialogflow's API for each conversational turn to send end-user expressions and receive intent matches.

- **Processing flow**:
  1. End-user types/speaks an expression
  2. Your service sends the expression to Dialogflow in a detect intent request message
  3. Dialogflow sends a detect intent response message (contains matched intent, action, parameters, response)
  4. Your service performs actions (database queries, external API calls)
  5. Your service sends a response to the end-user
  6. End-user sees/hears the response

## 5. Key Diagrams

- Basic flow for intent matching and responding
- Example using context for a banking agent
- Processing flow for fulfillment
- Processing flow when interacting with the API