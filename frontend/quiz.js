const questions = [
  { key: "sleep_hours", text: "How many hours did you sleep last night?", hint: "Dataset feature: sleep_hours", min: 0, max: 12, step: 0.5, unit: "hours" },
  { key: "screen_time", text: "How many hours of screen time today?", hint: "Dataset feature: screen_time", min: 0, max: 13, step: 0.5, unit: "hours" },
  { key: "exercise_minutes", text: "How many minutes did you exercise today?", hint: "Dataset feature: exercise_minutes", min: 0, max: 150, step: 5, unit: "min" },
  { key: "daily_pending_tasks", text: "How many pending tasks do you have today?", hint: "Dataset feature: daily_pending_tasks", min: 0, max: 10, step: 1, unit: "tasks" },
  { key: "interruptions", text: "How many interruptions did you face today?", hint: "Dataset feature: interruptions", min: 0, max: 15, step: 1, unit: "count" },
  { key: "fatigue_level", text: "How fatigued do you feel right now?", hint: "Dataset feature: fatigue_level (0-10)", min: 0, max: 10, step: 1, unit: "/10" },
  { key: "social_hours", text: "How many hours of social interaction today?", hint: "Dataset feature: social_hours", min: 0, max: 6, step: 0.5, unit: "hours" },
  { key: "coffee_cups", text: "How many cups of coffee today?", hint: "Dataset feature: coffee_cups", min: 0, max: 6, step: 1, unit: "cups" },
  { key: "diet_quality", text: "How would you rate your diet quality today?", hint: "Dataset feature: diet_quality", type: "select", options: ["poor", "average", "good"], unit: "" },
  { key: "weather", text: "What weather best matches your day?", hint: "Dataset feature: weather", type: "select", options: ["sunny", "cloudy", "rainy", "snowy"], unit: "" },
  { key: "mood_score", text: "How is your mood overall today?", hint: "Dataset feature: mood_score (0-10)", min: 0, max: 10, step: 1, unit: "/10" },
];

let currentQuestionIndex = 0;
const userData = {};

const questionEl = document.getElementById("question");
const phaseEl = document.getElementById("phase");
const hintEl = document.getElementById("hint");
const progressEl = document.getElementById("progress");
const inputEl = document.getElementById("answerInput");
const selectEl = document.getElementById("answerSelect");
const valueEl = document.getElementById("answerValue");
const minLabelEl = document.getElementById("minLabel");
const maxLabelEl = document.getElementById("maxLabel");
const unitLabelEl = document.getElementById("unitLabel");
const backBtn = document.getElementById("backBtn");

function formatValue(value, step) {
  if (Number(step) < 1) return Number(value).toFixed(1);
  return String(Math.round(Number(value)));
}

function updateValue(value) {
  const question = questions[currentQuestionIndex];
  valueEl.textContent = formatValue(value, question.step);
}

function updateSelectValue(value) {
  valueEl.textContent = value;
}

function setQuestionInput(question) {
  const isSelect = question.type === "select";
  inputEl.hidden = isSelect;
  selectEl.hidden = !isSelect;

  if (isSelect) {
    selectEl.innerHTML = question.options.map(opt => `<option value="${opt}">${opt}</option>`).join("");
    const savedValue = userData[question.key];
    selectEl.value = savedValue || question.options[0];
    updateSelectValue(selectEl.value);
    minLabelEl.innerText = question.options[0];
    maxLabelEl.innerText = question.options[question.options.length - 1];
    unitLabelEl.innerText = "";
    return;
  }

  const savedValue = userData[question.key];
  const currentValue = savedValue !== undefined ? savedValue : question.min;
  inputEl.min = question.min;
  inputEl.max = question.max;
  inputEl.step = question.step;
  inputEl.value = currentValue;
  minLabelEl.innerText = String(question.min);
  maxLabelEl.innerText = String(question.max);
  unitLabelEl.innerText = question.unit ? ` ${question.unit}` : "";
  updateValue(currentValue);
}

function showQuestion() {
  const question = questions[currentQuestionIndex];
  questionEl.innerText = question.text;
  phaseEl.innerText = "Regression Input";
  hintEl.innerText = question.hint;
  progressEl.innerText = `Question ${currentQuestionIndex + 1} of ${questions.length}`;
  setQuestionInput(question);
  backBtn.disabled = currentQuestionIndex === 0;
}

function nextQuestion() {
  const question = questions[currentQuestionIndex];
  userData[question.key] = question.type === "select" ? selectEl.value : Number(inputEl.value);

  currentQuestionIndex += 1;
  if (currentQuestionIndex < questions.length) {
    showQuestion();
    return;
  }
  finishQuiz();
}

function previousQuestion() {
  if (currentQuestionIndex === 0) return;
  currentQuestionIndex -= 1;
  showQuestion();
}

function finishQuiz() {
  localStorage.setItem("cognovoidQuizData", JSON.stringify(userData));
  document.querySelector(".quiz-container").innerHTML = `
    <h2>Quiz Completed</h2>
    <p>Your regression-model inputs are saved.</p>
    <div class="actions">
      <button class="btn primary" onclick="goToResults()">See Dashboard</button>
    </div>
  `;
}

function goToResults() {
  window.location.href = "result.html";
}

showQuestion();
