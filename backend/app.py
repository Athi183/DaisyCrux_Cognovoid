from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)  # Allow requests from all origins

# Load trained model & encoder
model = pickle.load(open("model.pkl", "rb"))
le = pickle.load(open("label_encoder.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    print("Received JSON:", data)

    # Mapping frontend quiz keys to model features
    mapped_data = {
        "Work_Hours_Per_Week": float(data.get("workHours", 0)),
        "Social_Media_Hours_Day": float(data.get("screen", 0)),
        "Work_Stress_Level": float(data.get("stress", 0)),
        "Sleep_Hours_Night": float(data.get("sleep", 0)),
        "Screen_Time_Hours_Day": float(data.get("screen", 0)),  # same as Social_Media_Hours_Day
        "Loneliness": float(data.get("loneliness", 0)),
        "Social_Support": float(data.get("socialSupport", 0))
    }

    # Convert to NumPy array
    features = np.array([[
        mapped_data["Work_Hours_Per_Week"],
        mapped_data["Social_Media_Hours_Day"],
        mapped_data["Work_Stress_Level"],
        mapped_data["Sleep_Hours_Night"],
        mapped_data["Screen_Time_Hours_Day"],
        mapped_data["Loneliness"],
        mapped_data["Social_Support"]
    ]])

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

        # Return JSON with only native Python types
        return jsonify({
            "state": mental_state,
            "message": messages.get(mental_state, "Be mindful of your mental state.")
        })

    except Exception as e:
        # Return error info for debugging
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)