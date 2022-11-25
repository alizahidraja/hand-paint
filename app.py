from flask import Flask, request, make_response, render_template, Response
import numpy as np
from camera import get_frame
from flask import send_file

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


def generate():
    while True:
        frame = get_frame()

        yield(b'--frame\r\n'
              b'Content-Type:  image/jpeg\r  \n\r\n' + frame +
              b'\r\n\r\n')

@app.route('/ss')
def ss():
    frame = get_frame()
    with open("ss.jpg", "wb") as binary_file:
        # Write bytes to file
        binary_file.write(frame)

    return send_file("ss.jpg", as_attachment=True)

@app.route("/video_feed")
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
