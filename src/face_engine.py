import cv2

class FaceDetector:
    def __init__(self):
        self.detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def detect(self, gray):
        return self.detector.detectMultiScale(gray, 1.3, 5)
