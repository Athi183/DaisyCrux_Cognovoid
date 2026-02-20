from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)  # Allow requests from all origins

# Load trained model & encoder
model = pickle.load(open("model.pkl", "rb"))
le = pickle.load(open("label_encoder.pkl", "rb"))

FEATURES = [
    "Work_Hours_Per_Week",
    "Social_Media_Hours_Day",
    "Work_Stress_Level",
    "Sleep_Hours_Night",
    "Screen_Time_Hours_Day",
    "Loneliness",
    "Social_Support",
]

FEATURE_RANGES = {
    "Work_Hours_Per_Week": (0, 80),
    "Social_Media_Hours_Day": (0, 12),
    "Work_Stress_Level": (0, 5),
    "Sleep_Hours_Night": (0, 10),
    "Screen_Time_Hours_Day": (0, 12),
    "Loneliness": (0, 5),
    "Social_Support": (0, 5),
}

POSITIVE_FEATURES = {"Sleep_Hours_Night", "Social_Support"}


def _to_float(data, *keys):
    for key in keys:
        if key in data and data[key] is not None:
            return float(data[key])
    return 0.0


def _scaled(value, min_val, max_val, invert=False):
    if max_val <= min_val:
        return 0
    clamped = max(min_val, min(max_val, value))
    scaled = ((clamped - min_val) / (max_val - min_val)) * 100.0
    if invert:
        scaled = 100.0 - scaled
    return int(round(scaled))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    print("Received JSON:", data)

    # Accepts either raw quiz keys or already mapped feature keys
    mapped_data = {
        "Work_Hours_Per_Week": _to_float(data, "workHours", "Work_Hours_Per_Week"),
        "Social_Media_Hours_Day": _to_float(data, "screen", "Social_Media_Hours_Day"),
        "Work_Stress_Level": _to_float(data, "stress", "Work_Stress_Level"),
        "Sleep_Hours_Night": _to_float(data, "sleep", "Sleep_Hours_Night"),
        "Screen_Time_Hours_Day": _to_float(data, "screen", "Screen_Time_Hours_Day"),
        "Loneliness": _to_float(data, "loneliness", "Loneliness"),
        "Social_Support": _to_float(data, "socialSupport", "Social_Support"),
    }

    # Convert to NumPy array
    features = np.array([[mapped_data[name] for name in FEATURES]])

    try:
        # Predict
        prediction = model.predict(features)

        # Convert NumPy int to Python int
        prediction_int = int(np.asscalar(prediction)) if hasattr(np, 'asscalar') else int(prediction[0])

        # Decode label and ensure it's a Python str
        mental_state = str(le.inverse_transform([prediction_int])[0])

        # Generalized messages
        messages = {
            "Calm": "You are in a balanced state. Keep it up! 🌟",
            "Stressed": "You seem stressed. Take a short break or deep breath. 🧘‍♂️",
            "Angry": "High emotional activation detected. Avoid important decisions now. ⚠️",
            "Impulsive": "Your responses show impulsivity. Pause before acting. ⏸️"
        }

        risk_by_state = {"Calm": 20, "Stressed": 72, "Angry": 86, "Impulsive": 78}
        base_risk = risk_by_state.get(mental_state, 50)

        feature_scores = {}
        for feature_name in FEATURES:
            min_val, max_val = FEATURE_RANGES[feature_name]
            feature_scores[feature_name] = _scaled(
                mapped_data[feature_name],
                min_val,
                max_val,
                invert=(feature_name in POSITIVE_FEATURES),
            )

        risk_score = int(round(sum(feature_scores.values()) / len(feature_scores)))
        risk_score = int(round((risk_score + base_risk) / 2))

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(features)[0]
            class_labels = le.inverse_transform(np.arange(len(probabilities)))
            proba_by_state = {
                str(class_labels[idx]): float(probabilities[idx])
                for idx in range(len(probabilities))
            }
        else:
            proba_by_state = {}

        return jsonify({
            "state": mental_state,
            "message": messages.get(mental_state, "Be mindful of your mental state."),
            "risk_score": risk_score,
            "inputs": mapped_data,
            "feature_scores": feature_scores,
            "state_probabilities": proba_by_state,
        })

    except Exception as e:
        # Return error info for debugging
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
