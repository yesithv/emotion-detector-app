# Local emotion detection (no external Watson/IBM endpoint required).
#
# Usage:
#   from EmotionDetection import emotion_detector
#   emotion_detector("I love this new technology.")
#
# The model is loaded lazily and cached, so the first call downloads/loads it
# and subsequent calls are fast.

from functools import lru_cache

# Use the operating system's trust store so downloads work behind a corporate
# proxy/VPN that performs SSL inspection with its own root CA. Harmless if no
# proxy is present.
try:
    import truststore

    truststore.inject_into_ssl()
except ImportError:
    pass

# Emotions the application reports, matching the original Watson output shape.
TARGET_EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")

_EMPTY_RESULT = {
    "anger": None,
    "disgust": None,
    "fear": None,
    "joy": None,
    "sadness": None,
    "dominant_emotion": None,
}


@lru_cache(maxsize=1)
def _get_classifier():
    """Load the Hugging Face emotion classifier once and reuse it."""
    from transformers import pipeline

    return pipeline(
        task="text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=None,  # return the full probability distribution
    )


def emotion_detector(text_to_analyze):
    """
    Analyze the emotion of a piece of text using a local model.

    Returns a dict with a score for each target emotion plus the dominant one,
    or a dict of Nones when the input is blank/invalid.
    """
    if not text_to_analyze or not text_to_analyze.strip():
        return dict(_EMPTY_RESULT)

    classifier = _get_classifier()
    predictions = classifier(text_to_analyze)[0]  # list of {label, score}

    scores = {item["label"]: item["score"] for item in predictions}
    emotions = {emotion: scores.get(emotion, 0.0) for emotion in TARGET_EMOTIONS}
    dominant_emotion = max(emotions, key=emotions.get)

    result = dict(emotions)
    result["dominant_emotion"] = dominant_emotion
    return result
