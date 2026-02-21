from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq

app = Flask(__name__)
CORS(app)
load_dotenv()

model = pickle.load(open("regression_model.pkl", "rb"))
meta = pickle.load(open("regression_meta.pkl", "rb"))
MODEL_FEATURES = meta["features"]
FEATURE_COLUMNS = meta["feature_columns"]
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
CHAT_PROMPT = """
You are Cognovoid — a calm rational companion.

If user sounds anxious:
- First reduce stress.
- Keep sentences short.
- Use gentle tone.
- Then guide logically.

If user wants to share story:
- Be warm and conversational.

Always respond in chat style.
Use small paragraphs.
Do not write long essays.
"""

FEATURE_RANGES = {
    "sleep_hours": (0, 12),
    "screen_time": (0, 13),
    "exercise_minutes": (0, 150),
    "daily_pending_tasks": (0, 10),
    "interruptions": (0, 15),
    "fatigue_level": (0, 10),
    "social_hours": (0, 6),
    "coffee_cups": (0, 6),
    "mood_score": (0, 10),
}
POSITIVE_FEATURES = {"sleep_hours", "exercise_minutes", "social_hours", "mood_score"}
DIET_RISK = {"poor": 80, "average": 45, "good": 20}
WEATHER_RISK = {"sunny": 20, "cloudy": 40, "rainy": 55, "snowy": 60}


def _to_float(data, key, default=0.0):
    value = data.get(key, default)
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _scaled(value, min_val, max_val, invert=False):
    if max_val <= min_val:
        return 0
    clamped = max(min_val, min(max_val, float(value)))
    scaled = ((clamped - min_val) / (max_val - min_val)) * 100.0
    if invert:
        scaled = 100.0 - scaled
    return int(round(scaled))


def _risk_band(score):
    if score <= 30:
        return "Low"
    if score <= 55:
        return "Moderate"
    if score <= 75:
        return "Elevated"
    return "High"


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}

    # Build feature row aligned to synthetic dataset schema.
    inputs = {
        "sleep_hours": _to_float(data, "sleep_hours", 7.0),
        "screen_time": _to_float(data, "screen_time", 4.0),
        "exercise_minutes": _to_float(data, "exercise_minutes", 20.0),
        "daily_pending_tasks": _to_float(data, "daily_pending_tasks", 3.0),
        "interruptions": _to_float(data, "interruptions", 5.0),
        "fatigue_level": _to_float(data, "fatigue_level", 5.0),
        "social_hours": _to_float(data, "social_hours", 2.0),
        "coffee_cups": _to_float(data, "coffee_cups", 1.0),
        "diet_quality": str(data.get("diet_quality", "average")).strip().lower(),
        "weather": str(data.get("weather", "cloudy")).strip().lower(),
        "mood_score": _to_float(data, "mood_score", 5.0),
    }
    if inputs["diet_quality"] not in DIET_RISK:
        inputs["diet_quality"] = "average"
    if inputs["weather"] not in WEATHER_RISK:
        inputs["weather"] = "cloudy"

    try:
        row = pd.DataFrame([inputs], columns=MODEL_FEATURES)
        encoded = pd.get_dummies(row, columns=meta["categorical"], dtype=float)
        encoded = encoded.reindex(columns=FEATURE_COLUMNS, fill_value=0.0)

        predicted_stress = float(model.predict(encoded)[0])
        predicted_stress = max(0.0, min(10.0, predicted_stress))
        model_risk = predicted_stress * 10.0

        feature_scores = {}
        for feature_name in FEATURE_RANGES:
            min_val, max_val = FEATURE_RANGES[feature_name]
            feature_scores[feature_name] = _scaled(
                inputs[feature_name],
                min_val,
                max_val,
                invert=(feature_name in POSITIVE_FEATURES),
            )
        feature_scores["diet_quality"] = DIET_RISK[inputs["diet_quality"]]
        feature_scores["weather"] = WEATHER_RISK[inputs["weather"]]
        feature_risk = sum(feature_scores.values()) / len(feature_scores)

        risk_score = int(round(max(0, min(100, (0.7 * model_risk) + (0.3 * feature_risk)))))
        band = _risk_band(risk_score)
        message = (
            f"Predicted stress level is {predicted_stress:.1f}/10. "
            f"Current risk band: {band}."
        )

        extra_guidance = []
        if inputs["sleep_hours"] < 6:
            extra_guidance.append("Low sleep detected: prioritize a recovery sleep window.")
        if inputs["exercise_minutes"] < 10:
            extra_guidance.append("Very low movement today: a short walk can reduce stress load.")
        if inputs["social_hours"] < 1:
            extra_guidance.append("Low social time: one check-in can improve emotional buffering.")

        return jsonify({
            "state": f"{band} Stress Outlook",
            "risk_score": risk_score,
            "predicted_stress_level": round(predicted_stress, 2),
            "model_risk_component": round(model_risk, 2),
            "feature_risk_component": round(feature_risk, 2),
            "inputs": inputs,
            "feature_scores": feature_scores,
            "message": message,
            "extra_guidance": extra_guidance,
        })
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = str(data.get("message", "")).strip()
    if not user_message:
        return jsonify({"error": "message is required"}), 400
    if groq_client is None:
        return jsonify({"error": "GROQ_API_KEY is not configured on the backend."}), 500
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": CHAT_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.6,
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as exc:
        return jsonify({"error": f"chat request failed: {exc}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
