/**
 * Hotel Booking Chatbot — Chat Interface JavaScript
 *
 * Handles sending messages, displaying responses, typing indicators,
 * quick replies, and smooth scrolling.
 */

// ---------- DOM References ----------
const messagesArea = document.getElementById("messages");
const userInput    = document.getElementById("userInput");
const sendBtn      = document.getElementById("sendBtn");

// ---------- Send Message ----------

/**
 * Send a message to the chatbot backend.
 * @param {string} [text] - Message text. If omitted, reads from the input field.
 */
function sendMessage(text) {
    const message = text || userInput.value.trim();
    if (!message) return;

    // Clear input field
    userInput.value = "";

    // Remove any existing quick replies
    removeQuickReplies();

    // Add user bubble
    addMessage(message, "user");

    // Show typing indicator
    showTyping();

    // Scroll to bottom
    scrollToBottom();

    // Send to backend
    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message }),
    })
    .then((res) => {
        if (!res.ok) throw new Error("Server error");
        return res.json();
    })
    .then((data) => {
        // Hide typing indicator
        hideTyping();

        // Add bot response
        addMessage(data.response, "bot");

        // Show quick replies if provided
        if (data.quick_replies && data.quick_replies.length > 0) {
            addQuickReplies(data.quick_replies);
        }

        // Scroll to bottom
        scrollToBottom();
    })
    .catch((err) => {
        console.error("Chat error:", err);
        hideTyping();
        addMessage(
            "Sorry, something went wrong. Please try again! 😅",
            "bot"
        );
        scrollToBottom();
    });
}

// ---------- Add Message Bubble ----------

/**
 * Create and append a message bubble to the chat.
 * @param {string} text - Message content.
 * @param {string} sender - "bot" or "user".
 */
function addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}-message`;

    if (sender === "bot") {
        const avatar = document.createElement("span");
        avatar.className = "avatar";
        avatar.textContent = "🤖";
        messageDiv.appendChild(avatar);
    }

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.textContent = text;
    messageDiv.appendChild(bubble);

    messagesArea.appendChild(messageDiv);
}

// ---------- Typing Indicator ----------

/** Show the animated typing indicator. */
function showTyping() {
    const typing = document.createElement("div");
    typing.className = "typing-indicator";
    typing.id = "typingIndicator";

    const avatar = document.createElement("span");
    avatar.className = "avatar";
    avatar.textContent = "🤖";
    typing.appendChild(avatar);

    const dots = document.createElement("div");
    dots.className = "typing-dots";
    dots.innerHTML = "<span></span><span></span><span></span>";
    typing.appendChild(dots);

    messagesArea.appendChild(typing);
    scrollToBottom();
}

/** Remove the typing indicator. */
function hideTyping() {
    const typing = document.getElementById("typingIndicator");
    if (typing) typing.remove();
}

// ---------- Quick Replies ----------

/**
 * Display quick-reply pill buttons below the last bot message.
 * @param {string[]} replies - Array of quick reply text options.
 */
function addQuickReplies(replies) {
    removeQuickReplies();

    const container = document.createElement("div");
    container.className = "quick-replies";
    container.id = "quickReplies";

    replies.forEach((text) => {
        const btn = document.createElement("button");
        btn.className = "quick-reply-btn";
        btn.textContent = text;
        btn.addEventListener("click", () => sendMessage(text));
        container.appendChild(btn);
    });

    messagesArea.appendChild(container);
    scrollToBottom();
}

/** Remove existing quick reply buttons. */
function removeQuickReplies() {
    // Remove dynamic quick replies
    const existing = document.getElementById("quickReplies");
    if (existing) existing.remove();

    // Also remove the initial quick replies (from HTML)
    const initial = document.getElementById("initialQuickReplies");
    if (initial) initial.remove();
}

// ---------- Scroll ----------

/** Smoothly scroll the message area to the bottom. */
function scrollToBottom() {
    setTimeout(() => {
        messagesArea.scrollTo({
            top: messagesArea.scrollHeight,
            behavior: "smooth",
        });
    }, 50);
}

// ---------- Event Listeners ----------

// Enter key sends message
userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
    }
});

// Auto-focus input
userInput.focus();

// Scroll to bottom on page load
scrollToBottom();
