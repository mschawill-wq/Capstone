import cv2
from flask import Flask, Response

app = Flask(__name__)

# Open desktop webcam
camera = cv2.VideoCapture(0)

# Camera settings
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
camera.set(cv2.CAP_PROP_FPS, 30)


def generate_frames():
    while True:
        success, frame = camera.read()

        if not success:
            continue

        # Compress frame to JPEG
        ret, buffer = cv2.imencode(
            '.jpg',
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, 80]
        )

        if not ret:
            continue

        frame_bytes = buffer.tobytes()

        # Send frame as MJPEG stream
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + frame_bytes
            + b'\r\n'
        )


@app.route('/')
def index():
    return "Camera server is running"


@app.route('/video_feed')
def video_feed():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=True
    )