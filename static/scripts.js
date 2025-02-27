async function sendMessage() {
    const userInput = document.getElementById('user-input').value.trim();
    if (!userInput) {
        alert("Please provide a valid input.");
        return;
    }

    const chatBox = document.getElementById('chat-box');
    const spinner = document.getElementById('spinner');

    // Display user message
    chatBox.innerHTML += `<div class="user-message"><p>${userInput}</p></div>`;

    // Show spinner
    spinner.style.display = 'block';

    // Clear input
    document.getElementById('user-input').value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: userInput })
        });

        const data = await response.json();
        const botMessage = data.response || "I couldn't find relevant information.";

        // Hide spinner
        spinner.style.display = 'none';

        // Display bot message
        chatBox.innerHTML += `<div class="bot-message"><p>${botMessage}</p></div>`;
    } catch (error) {
        console.error('🔥 Error:', error);
        spinner.style.display = 'none';
        chatBox.innerHTML += `<div class="bot-message"><p>I'm experiencing technical difficulties. Please try again later.</p></div>`;
    }

    // Scroll to the bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}
