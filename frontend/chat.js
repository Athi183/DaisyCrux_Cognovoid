const chatBox = document.getElementById("chatBox");
let hasSentFirstMessage = false;

function addMessage(text, sender) {
    const message = document.createElement("div");
    message.classList.add("message", sender);
    message.innerText = text;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {

    const messageInput = document.getElementById("messageInput");
    const userMessage = messageInput.value.trim();

    if (!userMessage) return;

    addMessage(userMessage, "user");
    if (!hasSentFirstMessage) {
        const level2Btn = document.getElementById("level2Btn");
        level2Btn.classList.remove("hidden");
        hasSentFirstMessage = true;
    }
    messageInput.value = "";  // clear input

    const loading = document.createElement("div");
    loading.classList.add("message", "bot");
    loading.innerText = "Thinking...";
    chatBox.appendChild(loading);

    try {
        const response = await fetch("http://localhost:3000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: userMessage
            })
        });

        const data = await response.json();
        chatBox.removeChild(loading);

        if (!response.ok) {
            addMessage("Server error.", "bot");
            return;
        }

        addMessage(data.reply, "bot");

    } catch (error) {
        chatBox.removeChild(loading);
        addMessage("Connection error. Is backend running?", "bot");
    }
}

function goToLevel2() {
    window.location.href = "quiz.html";
}
document.getElementById("messageInput")
.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
