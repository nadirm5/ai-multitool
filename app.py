from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    mode = data.get("mode")
    message = data.get("message")

    try:
        if mode == "text":
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message}]
            )
            return jsonify({"reply": response.choices[0].message.content})

        elif mode == "image":
            response = client.images.generate(
                prompt=message,
                n=1,
                size="512x512"
            )
            return jsonify({"image_url": response.data[0].url})

        else:
            return jsonify({"error": "Mode invalide"}), 400

    except Exception as e:
        return jsonify({"error": "Erreur serveur: " + str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
