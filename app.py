from flask import Flask, render_template, request, jsonify
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    mode = data.get("mode")
    message = data.get("message")

    if mode == "text":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    elif mode == "image":
        response = openai.Image.create(
            prompt=message,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        return jsonify({"image_url": image_url})

    else:
        return jsonify({"error": "Mode invalide"}), 400

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
