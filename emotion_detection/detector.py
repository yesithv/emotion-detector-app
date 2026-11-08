from abc import ABC, abstractmethod

from emotion_detection.result import EmotionResult


class EmotionDetector(ABC):
    @abstractmethod
    def detect(self, text: str) -> EmotionResult:
        """Detect the emotions expressed in the provided text."""
        raise NotImplementedError
