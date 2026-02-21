from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# ========================
# 1️⃣ Cognovoid ML Prediction Setup
# ========================

app = Flask(__name__)
CORS(app)

# Load ML model and label encoder
model = pickle.load(open("model.pkl", "rb"))
le = pickle.load(open("label_encoder.pkl", "rb"))

MODEL_FEATURES = [
    "sleep",
    "stress",
    "mood",
    "focus",
    "screen",
    "anxiety",
    "fatigue",
]

EXTRA_FEATURES = ["loneliness", "socialSupport", "workHours", "socialMedia", "screenTime"]

FEATURE_ALIASES = {
    "sleep": ["sleep", "Sleep_Hours_Night"],
    "stress": ["stress", "Work_Stress_Level"],
    "mood": ["mood"],
    "focus": ["focus"],
    "screen": ["screen", "screenTime", "Screen_Time_Hours_Day"],
    "anxiety": ["anxiety"],
    "fatigue": ["fatigue"],
}

FEATURE_RANGES = {
    "sleep": (0, 12),
    "stress": (0, 5),
    "mood": (0, 5),
    "focus": (0, 5),
    "screen": (0, 16),
    "anxiety": (0, 5),
    "fatigue": (0, 5),
}

POSITIVE_FEATURES = {"sleep", "mood", "focus"}


def _get_float(payload, keys, default=0.0):
    for key in keys:
        value = payload.get(key)
        if value is None:
            continue
        try:
            return float(value)
        except (TypeError, ValueError):
            continue
    return float(default)


def _state_risk_weight(state_label):
    text = str(state_label).strip().lower()
    if "calm" in text:
        return 10
    if "stress" in text:
        return 70
    if "angry" in text:
        return 90
    if "impuls" in text:
        return 80
    return None


def _scaled(value, min_val, max_val, invert=False):
    if max_val <= min_val:
        return 0
    clamped = max(min_val, min(max_val, float(value)))
    scaled = ((clamped - min_val) / (max_val - min_val)) * 100.0
    if invert:
        scaled = 100.0 - scaled
    return int(round(scaled))


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}

    feature_values = []
    missing_features = []
    for feat in MODEL_FEATURES:
        val = _get_float(data, FEATURE_ALIASES[feat], default=0.0)
        if all(data.get(alias) is None for alias in FEATURE_ALIASES[feat]):
            missing_features.append(feat)
        feature_values.append(val)
    core_inputs = dict(zip(MODEL_FEATURES, feature_values))

    features_array = np.array([feature_values], dtype=float)

    try:
        prediction = model.predict(features_array)
        prediction_int = int(prediction[0])
        mental_state = str(le.inverse_transform([prediction_int])[0])

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(features_array)[0]
            class_labels = le.inverse_transform(np.arange(len(probabilities)))
            proba_by_state = {str(class_labels[i]): float(probabilities[i]) for i in range(len(probabilities))}
            weighted_risk = 0.0
            unknown_states = []
            for idx, label in enumerate(class_labels):
                weight = _state_risk_weight(label)
                if weight is None:
                    unknown_states.append(idx)
                else:
                    weighted_risk += float(probabilities[idx]) * weight
            if unknown_states:
                fallback_weights = np.linspace(20, 90, len(class_labels))
                for idx in unknown_states:
                    weighted_risk += float(probabilities[idx]) * float(fallback_weights[idx])
            risk_score = int(round(max(0, min(100, weighted_risk))))
        else:
            proba_by_state = {}
            fallback_weight = _state_risk_weight(mental_state)
            risk_score = int(fallback_weight if fallback_weight is not None else 50)

        extras = {
            "loneliness": _get_float(data, ["loneliness", "Loneliness"], 0.0),
            "socialSupport": _get_float(data, ["socialSupport", "Social_Support"], 0.0),
            "workHours": _get_float(data, ["workHours", "Work_Hours_Per_Week"], 0.0),
            "socialMedia": _get_float(data, ["socialMedia", "Social_Media_Hours_Day"], 0.0),
            "screenTime": _get_float(data, ["screenTime", "Screen_Time_Hours_Day", "screen"], 0.0),
        }
        extra_guidance = []
        if extras["loneliness"] >= 3:
            extra_guidance.append("High loneliness: consider social interaction.")
        if extras["socialSupport"] <= 2:
            extra_guidance.append("Low support: reach out to friends/family.")
        if extras["workHours"] >= 55:
            extra_guidance.append("High workload: schedule recovery breaks.")

        feature_scores = {}
        for feature_name in MODEL_FEATURES:
            min_val, max_val = FEATURE_RANGES[feature_name]
            feature_scores[feature_name] = _scaled(
                core_inputs[feature_name],
                min_val,
                max_val,
                invert=(feature_name in POSITIVE_FEATURES),
            )

        messages = {
            "Calm": "Balanced mental state detected. Decision clarity is likely stable.",
            "Stressed": "Elevated emotional reactivity detected. Short recovery can improve decision clarity.",
            "Angry": "High emotional activation detected. Delay major choices until steadier.",
            "Impulsive": "Reduced decision inhibition detected. Add a pause before committing to actions.",
        }

        return jsonify({
            "state": mental_state,
            "risk_score": risk_score,
            "inputs_core": core_inputs,
            "inputs_extra": extras,
            "feature_scores": feature_scores,
            "message": messages.get(mental_state, "Be mindful of your current mental state."),
            "extra_guidance": extra_guidance,
            "state_probabilities": proba_by_state,
            "missing_features": missing_features
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========================
# 2️⃣ Cognovoid Groq Chatbot Setup
# ========================

PROMPT = """
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

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=api_key) if api_key else None


def generate_cognovoid_reply(user_message, client=None):
    if not user_message:
        raise ValueError("message is required")

    client = client or get_groq_client()
    if client is None:
        raise RuntimeError("GROQ_API_KEY is not configured on the backend.")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.6,
    )
    return response.choices[0].message.content


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = str(data.get("message", "")).strip()

    try:
        reply = generate_cognovoid_reply(user_message)
        return jsonify({"reply": reply})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": f"chat request failed: {exc}"}), 500


# ========================
# 3️⃣ Run the app
# ========================
if __name__ == "__main__":
    app.run(port=3000, debug=True)