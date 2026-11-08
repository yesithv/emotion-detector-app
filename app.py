"""
Flask server for the Emotion Detection application.

Run with:
    python app.py
"""

from dataclasses import asdict

from flask import Flask, jsonify, render_template, request

from emotion_detection.detector import EmotionDetector
from emotion_detection.implementations.transformers_detector import (
    TransformersEmotionDetector,
)

app = Flask("Emotion Detector")

# Swap the engine here, e.g. WatsonEmotionDetector() (IBM lab only).
detector: EmotionDetector = TransformersEmotionDetector()


@app.route("/emotionDetector")
def emotion_detector():
    """
    Detect the emotions of the text received in the textToAnalyze parameter.
    """
    text_to_analyze = request.args.get("textToAnalyze", "").strip()

    if not text_to_analyze:
        return jsonify({
            "error": "Invalid text! Please try again!"
        }), 400

    result = detector.detect(text_to_analyze)

    return jsonify(asdict(result))


@app.route("/")
def render_index_page():
    """
    Render the index page.
    """
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
