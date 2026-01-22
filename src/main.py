import cv2, os, csv, threading, time
from datetime import datetime

from src.camera import open_camera
from src.face_engine import FaceDetector
from src.recorder import Recorder
import src.stream_server as stream_server

def main():
    # Ensure log directory exists
    os.makedirs("data/logs", exist_ok=True)

    cap = open_camera()
    if cap is None or not cap.isOpened():
        print("Error: Could not open camera.")
        return

    detector = FaceDetector()
    recorder = Recorder()

    # Start the stream server in a separate thread
    threading.Thread(target=stream_server.start_server, daemon=True).start()

    last_capture_time = 0

    print("Starting camera streaming service...")
    print("Live stream available at http://localhost:5000/live")
    print("Press 'q' to quit.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detect(gray)

            today = datetime.now().strftime("%Y-%m-%d")
            face_dir = f"data/captured_faces/{today}"
            os.makedirs(face_dir, exist_ok=True)

            current_time = time.time()

            for (x, y, w, h) in faces:
                # Draw rectangle around detected faces
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Capture once every 5 seconds max
                if (current_time - last_capture_time) > 5:
                    face_img = frame[y : y + h, x : x + w]
                    timestamp = datetime.now().strftime("%H-%M-%S")
                    name = f"face_{timestamp}.jpg"
                    cv2.imwrite(f"{face_dir}/{name}", face_img)

                    # Log the capture
                    with open("data/logs/capture_log.csv", "a", newline="") as f:
                        csv.writer(f).writerow([name, datetime.now().isoformat()])

                    last_capture_time = current_time

            # Record the frame
            recorder.write(frame)

            # Update the latest frame for the stream server
            _, jpeg = cv2.imencode(".jpg", frame)
            stream_server.latest_frame = jpeg.tobytes()

            # Show live preview (if window is supported)
            try:
                cv2.imshow("Live Capture", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            except cv2.error:
                # Fallback for environments without GUI
                pass

    finally:
        print("Shutting down...")
        cap.release()
        recorder.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
