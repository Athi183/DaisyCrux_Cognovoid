from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# ========================
# Load trained model
# ========================

model = pickle.load(open("regression_model.pkl", "rb"))
meta = pickle.load(open("regression_meta.pkl", "rb"))

MODEL_FEATURES = meta["features"]

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

# ========================
# Utility functions
# ========================

def _get_float(payload, key, default=0.0):
    try:
        return float(payload.get(key, default))
    except (TypeError, ValueError):
        return float(default)


def _scaled(value, min_val, max_val, invert=False):
    if max_val <= min_val:
        return 0
    value = max(min_val, min(max_val, float(value)))
    score = ((value - min_val) / (max_val - min_val)) * 100
    if invert:
        score = 100 - score
    return int(round(score))


def get_mental_state(score):
    if score < 30:
        return "Calm"
    elif score < 60:
        return "Stressed"
    elif score < 80:
        return "Angry"
    else:
        return "Impulsive"


# ========================
# Groq Chatbot
# ========================

PROMPT = """
You are Cognovoid — a calm rational companion.

If user sounds anxious:
- First reduce stress.
- Keep sentences short.
- Use gentle tone.

If user wants to share story:
- Be warm and conversational.

Always respond in chat style.
Small paragraphs only.
"""


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=api_key) if api_key else None


def generate_cognovoid_reply(user_message):
    client = get_groq_client()
    if client is None:
        raise RuntimeError("GROQ_API_KEY not set.")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.6,
    )
    return response.choices[0].message.content


# ========================
# Single Main Route
# ========================

@app.route("/", methods=["GET", "POST"])
def main_route():

    # ---------- GET = Health check ----------
    if request.method == "GET":
        return jsonify({
            "status": "Cognovoid backend running 🚀",
            "usage": {
                "predict": "POST with action='predict' and feature data",
                "chat": "POST with action='chat' and message"
            }
        })

    # ---------- POST ----------
    data = request.get_json(silent=True) or {}
    action = data.get("action")

    # ===== Prediction =====
    if action == "predict":

        feature_values = []
        missing = []

        for feat in MODEL_FEATURES:
            if feat not in data:
                missing.append(feat)
            feature_values.append(_get_float(data, feat, 0.0))

        features_array = np.array([feature_values], dtype=float)

        try:
            prediction = model.predict(features_array)
            score = float(prediction[0])

            mental_state = get_mental_state(score)
            risk_score = int(max(0, min(100, score)))

            feature_scores = {}
            for feat in MODEL_FEATURES:
                min_val, max_val = FEATURE_RANGES.get(feat, (0, 10))
                feature_scores[feat] = _scaled(
                    data.get(feat, 0),
                    min_val,
                    max_val,
                    invert=(feat in POSITIVE_FEATURES),
                )

            messages = {
                "Calm": "Balanced mental state detected. Decision clarity is stable.",
                "Stressed": "Some stress detected. Short breaks can improve clarity.",
                "Angry": "High emotional activation detected. Delay major decisions.",
                "Impulsive": "Low inhibition detected. Pause before acting.",
            }

            return jsonify({
                "state": mental_state,
                "risk_score": risk_score,
                "feature_scores": feature_scores,
                "message": messages.get(mental_state),
                "missing_features": missing
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # ===== Chat =====
    elif action == "chat":
        user_message = str(data.get("message", "")).strip()

        if not user_message:
            return jsonify({"error": "message is required"}), 400

        try:
            reply = generate_cognovoid_reply(user_message)
            return jsonify({"reply": reply})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # ===== Invalid action =====
    else:
        return jsonify({
            "error": "Invalid action. Use 'predict' or 'chat'."
        }), 400


# ========================
# DO NOT use app.run() on Render
# ========================