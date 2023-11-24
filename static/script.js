document.addEventListener("DOMContentLoaded", function() {    
    // Add a welcome message when the page loads
    displayMessage("Welcome to Knowledge Management Chat assistant, I am here to help you with any internal queries related to our Organization.", "chatbot-message");
});

function getAnswer() {
    var userQuestion = document.getElementById("user-input").value;
    var chatbotAnswer;
    // For demonstration purposes, replace this with your actual fetch logic
    fetch("/get_answer", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "user_question=" + encodeURIComponent(userQuestion),
    })
    .then(response => response.json())
    .then(data => {
        displayMessage("You: " + userQuestion, "user-message");
        displayMessage(data.answer, "chatbot-message");
    });

    

    

    // Clear the input field
    document.getElementById("user-input").value = "";
}

// function displayMessage(message, senderClass) {
//     var chatHistory = document.getElementById("chat-history");
//     var messageDiv = document.createElement("div");
//     messageDiv.innerText = message;
//     messageDiv.classList.add("message", senderClass);
//     chatHistory.appendChild(messageDiv);
// }

function displayMessage(message, senderClass) {
    var chatHistory = document.getElementById("chat-history");
    var messageDiv = document.createElement("div");
    messageDiv.classList.add("message", senderClass);

    // Check if the message contains a hyperlink in the specified format
    var match = message.match(/\[([^\]]+)\]\(([^)]+)\)/);
    if (match) {
        // If it matches the format [text](url), extract text and display a custom message
        var dynamicMessage = message.substring(0, match.index);
        var linkText = match[1];
        var linkUrl = match[2];

        // Create a hyperlink element
        var link = document.createElement("a");
        link.href = linkUrl;
        link.target = "_blank"; // Open the link in a new tab
        link.textContent = linkText;

        // Append the dynamic message and the hyperlink to the messageDiv
        messageDiv.innerHTML = dynamicMessage;
        messageDiv.appendChild(link);
    } else {
        // If it's not in the specified format, display the entire message
        messageDiv.innerHTML = message;
    }

    chatHistory.appendChild(messageDiv);
}
