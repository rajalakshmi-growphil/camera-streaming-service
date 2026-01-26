import cv2, os, csv, threading, time
from datetime import datetime

from src.camera import open_camera
from src.face_engine import FaceDetector
from src.recorder import Recorder
import src.stream_server as stream_server


def main():
    os.makedirs("data/logs", exist_ok=True)

    cap = open_camera()
    if cap is None or not cap.isOpened():
        print("Error: Could not open camera.")
        return

    detector = FaceDetector(
        min_distance=80,        # distance threshold (pixels)
        cooldown_seconds=10     # same face cooldown
    )
    recorder = Recorder()

    threading.Thread(
        target=stream_server.start_server,
        daemon=True
    ).start()

    prev_time = time.time()

    print("Starting camera streaming service...")
    print("Live stream: http://localhost:5000/live")
    print("Press 'q' to quit.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # -------- FPS --------
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time
            print(f"FPS: {int(fps)}", end="\r")

            # -------- FACE DETECTION --------
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detect(gray)

            today = datetime.now().strftime("%Y-%m-%d")
            face_dir = f"data/captured_faces/{today}"
            os.makedirs(face_dir, exist_ok=True)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                if detector.should_capture(x, y, w, h):
                    face_img = frame[y:y + h, x:x + w]
                    timestamp = datetime.now().strftime("%H-%M-%S")
                    name = f"face_{timestamp}.jpg"
                    cv2.imwrite(f"{face_dir}/{name}", face_img)

                    with open("data/logs/capture_log.csv", "a", newline="") as f:
                        csv.writer(f).writerow([name, datetime.now().isoformat()])

            # -------- DRAW FPS --------
            cv2.putText(
                frame,
                f"FPS: {int(fps)}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            recorder.write(frame)

            _, jpeg = cv2.imencode(".jpg", frame)
            stream_server.latest_frame = jpeg.tobytes()

            try:
                cv2.imshow("Live Capture", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            except cv2.error:
                pass

    finally:
        print("\nShutting down...")
        cap.release()
        recorder.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
