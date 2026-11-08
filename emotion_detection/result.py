from dataclasses import dataclass

EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


@dataclass(frozen=True)
class EmotionResult:
    anger: float
    disgust: float
    fear: float
    joy: float
    sadness: float
    dominant_emotion: str
