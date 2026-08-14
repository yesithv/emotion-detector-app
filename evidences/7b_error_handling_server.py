

from flask import Flask, request, render_template

from EmotionDetector.final_project.EmotionDetection import emotion_detector

app = Flask('Emotion detection')

@app.route('/emotionDetector')
def emotion_detectioning():
    text = request.args.get('textToAnalyze')
    response = emotion_detector(text)
    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!"
    return (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )


@app.route("/")
def render_index_page():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)