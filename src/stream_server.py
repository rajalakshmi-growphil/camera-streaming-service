from flask import Flask, Response

app = Flask(__name__)
latest_frame = None

def generate():
    global latest_frame
    while True:
        if latest_frame is None:
            continue
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" +
               latest_frame + b"\r\n")

@app.route("/live")
def live():
    return Response(generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame")

def start_server():
    # Use 0.0.0.0 to make it accessible on the local network
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=False, use_reloader=False)
