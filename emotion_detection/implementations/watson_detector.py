import requests

from emotion_detection.detector import EmotionDetector
from emotion_detection.result import EMOTIONS, EmotionResult


class WatsonEmotionDetector(EmotionDetector):
    # Only reachable from inside the IBM Skills Network lab environment.
    API_URL = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )

    MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"

    def detect(self, text: str) -> EmotionResult:
        payload = {
            "raw_document": {
                "text": text
            }
        }

        headers = {
            "grpc-metadata-mm-model-id": self.MODEL_ID
        }

        response = requests.post(
            self.API_URL,
            json=payload,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        predictions = response.json()["emotionPredictions"][0]["emotion"]
        emotions = {emotion: predictions[emotion] for emotion in EMOTIONS}

        return EmotionResult(
            **emotions,
            dominant_emotion=max(emotions, key=emotions.get)
        )
