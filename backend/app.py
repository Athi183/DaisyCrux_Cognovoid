from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()  # load .env file

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    user_message = data.get("message")

    prompt = f"""
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

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.6
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Something went wrong"}), 500
if __name__ == "__main__":
    app.run(port=3000, debug=True)