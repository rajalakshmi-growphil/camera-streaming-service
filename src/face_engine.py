import cv2
import math
import time

class FaceDetector:
    def __init__(self, min_distance=80, cooldown_seconds=10):
        self.detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.min_distance = min_distance
        self.cooldown_seconds = cooldown_seconds
        self.recent_faces = []  # [(cx, cy, timestamp)]

    def detect(self, gray):
        return self.detector.detectMultiScale(gray, 1.3, 5)

    def should_capture(self, x, y, w, h):
        now = time.time()
        cx = x + w // 2
        cy = y + h // 2

        # Remove old face entries
        self.recent_faces = [
            (fx, fy, t)
            for (fx, fy, t) in self.recent_faces
            if now - t < self.cooldown_seconds
        ]

        for fx, fy, _ in self.recent_faces:
            dist = math.hypot(cx - fx, cy - fy)
            if dist < self.min_distance:
                return False  # Same face, too close

        # New face → remember it
        self.recent_faces.append((cx, cy, now))
        return True
