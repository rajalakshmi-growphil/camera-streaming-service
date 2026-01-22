import cv2, os
from datetime import datetime

class Recorder:
    def __init__(self):
        day = datetime.now().strftime("%Y-%m-%d")
        self.base = f"data/recordings/{day}"
        os.makedirs(self.base, exist_ok=True)

        name = datetime.now().strftime("cam_%H-%M-%S.mp4")
        self.writer = cv2.VideoWriter(
            f"{self.base}/{name}",
            cv2.VideoWriter_fourcc(*"mp4v"),
            20,
            (1280, 720)
        )

    def write(self, frame):
        self.writer.write(frame)

    def close(self):
        self.writer.release()
