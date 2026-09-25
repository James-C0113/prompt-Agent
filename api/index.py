from flask import Flask, request, jsonify
import os
import sys
import yaml

# Allow imports from src/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from prompt_optim_agent import BaseAgent

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "name": "PromptAgent",
        "status": "running",
        "message": "Prompt optimization API"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })


@app.route("/optimize", methods=["POST"])
def optimize():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "JSON body required"
            }), 400

        prompt = data.get("prompt")

        if not prompt:
            return jsonify({
                "error": "prompt is required"
            }), 400

        # Load the repository's configuration
        config_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "example_config.yaml"
        )

        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        # Override the initial prompt
        config["init_prompt"] = prompt

        # API keys should come from Vercel environment variables
        if config["base_model_setting"]["model_type"] == "openai":
            config["base_model_setting"]["api_key"] = os.environ.get(
                "OPENAI_API_KEY"
            )

        if config["optim_model_setting"]["model_type"] == "openai":
            config["optim_model_setting"]["api_key"] = os.environ.get(
                "OPENAI_API_KEY"
            )

        # Create PromptAgent
        agent = BaseAgent(**config)

        # Run optimization
        agent.run()

        return jsonify({
            "status": "completed",
            "message": "Prompt optimization completed"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500