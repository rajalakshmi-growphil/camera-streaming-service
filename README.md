# Camera Streaming Service (Simplified)

A live camera system that detects faces and saves face images daily from a live feed.

## Features

- ✅ **Live streaming**: Accessible via a web browser.
- ✅ **Face Detection**: Automatically detects faces in the live feed.
- ✅ **Daily Captures**: Saves detected face images in date-stamped folders.
- ✅ **Feed Recording**: Records the live feed into date-stamped folders.
- ✅ **Detailed Logs**: Maintains a log of all captured face images.

## Project Structure

```text
camera-streaming-service/
├── data/
│   ├── captured_faces/  # Daily folders for face images
│   ├── recordings/      # Daily folders for video recordings
│   └── logs/            # capture_log.csv
├── src/
│   ├── camera.py        # Camera initialization
│   ├── face_engine.py   # Face detection logic
│   ├── recorder.py      # Video recording logic
│   ├── stream_server.py # Flask live stream server
│   └── main.py          # Main application loop
├── requirements.txt
└── README.md
```

## Setup and Run

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the service**:
   ```bash
   python -B -m src.main
   ```

3. **View the live stream**:
   Open your browser and navigate to:
   [http://localhost:5000/live](http://localhost:5000/live)

## Configuration

- **Face Capture Frequency**: Modified in `src/main.py`. Currently set to capture a face image at most once every 5 seconds.
- **Resolution**: Set to 720p (1280x720) in `src/camera.py`.