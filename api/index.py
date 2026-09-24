from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "name": "PromptAgent",
        "status": "running",
        "description": "Automatic prompt optimization using MCTS"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })