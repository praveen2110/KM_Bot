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
        displayMessage( data.answer, "chatbot-message");
    });

    

    

    // Clear the input field
    document.getElementById("user-input").value = "";
}

function displayMessage(message, senderClass) {
    var chatHistory = document.getElementById("chat-history");
    var messageDiv = document.createElement("div");
    messageDiv.innerText = message;
    messageDiv.classList.add("message", senderClass);
    chatHistory.appendChild(messageDiv);
}