import unittest

from emotion_detection.implementations.transformers_detector import (
    TransformersEmotionDetector,
)


class TestTransformersEmotionDetector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.detector = TransformersEmotionDetector()

    def test_dominant_emotion(self):
        cases = {
            "I am glad this happened": "joy",
            "I am really mad about this": "anger",
            "I feel disgusted just hearing about this": "disgust",
            "I am so sad about this": "sadness",
            "I am really afraid that this will happen": "fear",
        }

        for text, expected in cases.items():
            with self.subTest(text=text):
                result = self.detector.detect(text)
                self.assertEqual(result.dominant_emotion, expected)

    def test_scores_are_probabilities(self):
        result = self.detector.detect("I love this new technology")

        for score in (result.anger, result.disgust, result.fear,
                      result.joy, result.sadness):
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 1)


if __name__ == "__main__":
    unittest.main()
