"""
Flask server for the Emotion Detection application.
"""

from flask import Flask, request, render_template

from EmotionDetection import emotion_detector

app = Flask('Emotion detection')

@app.route('/emotionDetector')
def emotion_detectioning():
    """
    Analyze the emotion of the provided text.
    """
    text = request.args.get('textToAnalyze')
    response = emotion_detector(text)
    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!"
    return (
        f"For the given statement, the system response is:<br>"
        f"'anger': {round(response['anger']*100, 2)} % <br>"
        f"'disgust': {round(response['disgust']*100, 2)} % <br>"
        f"'fear': {round(response['fear']*100, 2)} % <br>"
        f"'joy': {round(response['joy']*100, 2)} % <br>"
        f"'sadness': {round(response['sadness']*100, 2)} % <br>"
        f"The dominant emotion is <strong>{response['dominant_emotion']}</strong>."
    )


@app.route("/")
def render_index_page():
    """
    Render the index page.
    """
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
