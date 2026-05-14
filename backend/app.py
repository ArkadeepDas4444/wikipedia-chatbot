from flask import Flask, request, jsonify
from flask_cors import CORS
from backend import ask_question

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("message")

    try:
        response = ask_question(question)

        return jsonify({
            "response": response
        })

    except Exception as e:
        return jsonify({
            "response": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)