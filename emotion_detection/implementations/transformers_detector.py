from transformers import pipeline

from emotion_detection.detector import EmotionDetector
from emotion_detection.result import EMOTIONS, EmotionResult

# Use the OS trust store so the model download works behind SSL-inspecting proxies.
try:
    import truststore

    truststore.inject_into_ssl()
except ImportError:
    pass


class TransformersEmotionDetector(EmotionDetector):

    MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

    def __init__(self):
        self.classifier = pipeline(
            "text-classification",
            model=self.MODEL_NAME,
            top_k=None
        )

    def detect(self, text: str) -> EmotionResult:
        predictions = self.classifier([text])[0]
        scores = {item["label"]: item["score"] for item in predictions}

        # The model also predicts "neutral" and "surprise"; keep the course's 5 emotions.
        emotions = {emotion: scores.get(emotion, 0.0) for emotion in EMOTIONS}

        return EmotionResult(
            **emotions,
            dominant_emotion=max(emotions, key=emotions.get)
        )
