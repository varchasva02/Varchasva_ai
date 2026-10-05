from flask import Flask, request, jsonify
from flask_cors import CORS

from rag.pipeline import ask_varchasva


app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "message": "Varchasva AI API is running"
    })


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({
            "error": "Question is required"
        }), 400

    question = data["question"].strip()

    if not question:
        return jsonify({
            "error": "Question cannot be empty"
        }), 400

    try:
        answer = ask_varchasva(question)

        return jsonify({
            "question": question,
            "answer": answer
        })

    except Exception as e:
        error_message = str(e)
        app.logger.error("Error generating answer: %s", error_message)

        if "503" in error_message or "UNAVAILABLE" in error_message:
            return jsonify({
                "error": "The AI service is temporarily unavailable. Please try again shortly."
            }), 503

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            return jsonify({
                "error": "The AI service is temporarily unavailable due to high demand. Please try again shortly."
            }), 503

        return jsonify({
            "error": "Failed to generate answer. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False 
    )
