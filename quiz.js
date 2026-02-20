let questions = [
  { key: "sleep", text: "How many hours did you sleep last night?" },
  { key: "stress", text: "How stressed do you feel right now?" },
  { key: "mood", text: "How would you rate your mood today?" },
  { key: "focus", text: "How focused do you feel currently?" },
  { key: "screen", text: "How long was your screen time today?" }
];

let extraQuestions = {
  stress: { key: "anxiety", text: "Do you feel emotionally overwhelmed?" },
  sleep: { key: "fatigue", text: "Do you feel brain fog or tiredness?" }
};

let currentQuestionIndex = 0;
let userData = {};

const questionEl = document.getElementById("question");
const progressEl = document.getElementById("progress");

function showQuestion() {
  questionEl.innerText = questions[currentQuestionIndex].text;
  progressEl.innerText = `Question ${currentQuestionIndex + 1}`;
}

showQuestion();

function selectAnswer(value) {
  let currentKey = questions[currentQuestionIndex].key;
  userData[currentKey] = value;

  // Adaptive Logic
  if (currentKey === "stress" && value >= 4) {
    questions.splice(currentQuestionIndex + 1, 0, extraQuestions.stress);
  }

  if (currentKey === "sleep" && value <= 2) {
    questions.splice(currentQuestionIndex + 1, 0, extraQuestions.sleep);
  }

  currentQuestionIndex++;

  if (currentQuestionIndex < questions.length) {
    showQuestion();
  } else {
    finishQuiz();
  }
}

function finishQuiz() {
  console.log("User Data:", userData);

  // Temporary result display
  document.querySelector(".quiz-container").innerHTML = `
    <h2>Quiz Completed ✅</h2>
    <p>Your mental data has been recorded.</p>
    <button onclick="sendToBackend()">Analyze</button>
  `;
}

function sendToBackend() {
  fetch("http://localhost:5000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(userData)
  })
  .then(res => res.json())
  .then(data => {
    alert("Prediction: " + data.state);
  });
}