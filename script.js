
function sendMessage() {

    const mood = document.getElementById("mood").value;
    const scenario = document.getElementById("scenario").value;
    const chatBox = document.getElementById("chatBox");

    if (!mood || !scenario) {
        alert("Please select mood and describe your situation.");
        return;
    }

    // Show user message
    const userMsg = document.createElement("div");
    userMsg.className = "message user";
    userMsg.innerText = "Mood: " + mood + "\n" + scenario;
    chatBox.appendChild(userMsg);

    // Show loading message
    const botMsg = document.createElement("div");
    botMsg.className = "message bot";
    botMsg.innerText = "Thinking clearly...";
    chatBox.appendChild(botMsg);

    fetch("http://localhost:3000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            mood: mood,
            scenario: scenario
        })
    })
    .then(res => res.json())
    .then(data => {
        botMsg.innerText = data.reply;
    })
    .catch(error => {
        botMsg.innerText = "Server error. Check backend.";
        console.error(error);
    });
function startQuiz() {
    window.location.href = "quiz.html";
}};