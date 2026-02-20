
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

function showQuestion() {
  questionEl.innerText = questions[currentQuestionIndex].text;
  progressEl.innerText = `Question ${currentQuestionIndex + 1}`;

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

  // Adaptive Logic

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
    <button onclick="sendToBackend()">Analyze Your State</button>
  `;
}

// Map frontend keys to XGBoost model features and send to backend
function sendToBackend() {
  const mappedData = {
    Work_Hours_Per_Week: Number(userData.workHours || 0),
    Social_Media_Hours_Day: Number(userData.screen || 0),
    Work_Stress_Level: Number(userData.stress || 0),
    Sleep_Hours_Night: Number(userData.sleep || 0),
    Screen_Time_Hours_Day: Number(userData.screen || 0),
    Loneliness: Number(userData.loneliness || 0),
    Social_Support: Number(userData.socialSupport || 0)
  };

  fetch("http://localhost:5000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(mappedData)
  })
  .then(res => res.json())
  .then(data => {
    // Handle backend errors
    if(data.error){
      document.querySelector(".quiz-container").innerHTML = `
        <h2>Error ❌</h2>
        <p>${data.error}</p>
        <button onclick="location.reload()">Try Again</button>
      `;
      console.error("Backend Error:", data.error);
      return;
    }

    document.querySelector(".quiz-container").innerHTML = `
      <h2>Result: ${data.state || "Unknown"} ✅</h2>
      <p>${data.message || "No message returned."}</p>
      <button onclick="location.reload()">Try Again</button>
    `;
  })
  .catch(err => {
    document.querySelector(".quiz-container").innerHTML = `
      <h2>Network Error ❌</h2>
      <p>Could not reach backend.</p>
      <button onclick="location.reload()">Try Again</button>
    `;
    console.error("Fetch Error:", err);

  });
}};