// quiz.js

// Quiz questions aligned with ML model features
let questions = [
  { key: "sleep", text: "How many hours did you sleep last night?" },                     // Sleep_Hours_Night
  { key: "stress", text: "How stressed do you feel right now?" },                          // Work_Stress_Level
  { key: "screen", text: "How many hours did you spend on social media today?" },          // Social_Media_Hours_Day & Screen_Time_Hours_Day
  { key: "focus", text: "How focused do you feel currently?" },                             // Optional for future features
  { key: "workHours", text: "How many hours did you work/study this week?" },             // Work_Hours_Per_Week
  { key: "loneliness", text: "Do you feel lonely today? (0-5 scale)" },                  // Loneliness
  { key: "socialSupport", text: "Do you feel supported by friends/family? (0-5 scale)" } // Social_Support
];

// Extra adaptive questions based on responses
let extraQuestions = {
  stress: { key: "anxiety", text: "Do you feel emotionally overwhelmed? (0-5)" },
  sleep: { key: "fatigue", text: "Do you feel brain fog or extreme tiredness? (0-5)" },
  loneliness: { key: "isolation", text: "Are you avoiding social interactions? (0-5)" }
};

let currentQuestionIndex = 0;
let userData = {};

const questionEl = document.getElementById("question");
const progressEl = document.getElementById("progress");

// Show the current question
function showQuestion() {
  questionEl.innerText = questions[currentQuestionIndex].text;
  progressEl.innerText = `Question ${currentQuestionIndex + 1} of ${questions.length}`;
}

showQuestion();

// User selects an answer (number scale 0-5 or hours)
function selectAnswer(value) {
  let currentKey = questions[currentQuestionIndex].key;
  userData[currentKey] = value;

  // Adaptive logic
  if (currentKey === "stress" && value >= 4) {
    questions.splice(currentQuestionIndex + 1, 0, extraQuestions.stress);
  }

  if (currentKey === "sleep" && value <= 2) {
    questions.splice(currentQuestionIndex + 1, 0, extraQuestions.sleep);
  }

  if (currentKey === "loneliness" && value >= 3) {
    questions.splice(currentQuestionIndex + 1, 0, extraQuestions.loneliness);
  }

  currentQuestionIndex++;

  if (currentQuestionIndex < questions.length) {
    showQuestion();
  } else {
    finishQuiz();
  }
}

// Quiz finished
function finishQuiz() {
  console.log("User Data Collected:", userData);

  document.querySelector(".quiz-container").innerHTML = `
    <h2>Quiz Completed ✅</h2>
    <p>Your mental data has been recorded.</p>
    <button onclick="goToResults()">See Dashboard</button>
  `;
}

function goToResults() {
  localStorage.setItem("cognovoidQuizData", JSON.stringify(userData));
  window.location.href = "result.html";
}
