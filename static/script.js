document.addEventListener("DOMContentLoaded", function() {
    // Focus on the input field when the page loads
    document.getElementById("user-input").focus();

    // Add event listener for the Enter key
    document.getElementById("user-input").addEventListener("keydown", handleKeyPress);
});

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage(); // Send the message when Enter is pressed
    }
}

function sendMessage() {
    let inputField = document.getElementById("user-input");
    let userMessage = inputField.value.trim();
    if (userMessage === "") return; // Don't send an empty message

    let chatBox = document.getElementById("chat-box");

    // Append user message to chat box
    let userMessageElement = document.createElement("div");
    userMessageElement.className = "message user-message";
    userMessageElement.innerText = "You: " + userMessage;
    chatBox.appendChild(userMessageElement);

    // Clear input field after sending
    inputField.value = "";

    // Send the message to the backend (Flask)
    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        // Append bot's response to chat box
        let botMessageElement = document.createElement("div");
        botMessageElement.className = "message bot-message";
        botMessageElement.innerText = "LinuxSentinel: " + data.response;
        chatBox.appendChild(botMessageElement);

        // Scroll chat box to the bottom
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => console.error("Error:", error)); // Log any errors
}
