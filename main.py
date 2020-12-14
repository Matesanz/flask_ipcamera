import cv2
from flask import Flask, render_template, Response, Blueprint, redirect, url_for
from flask_login import login_required, current_user

class VideoCamera(object):
    def __init__(self, index: int = 0):

        self.video = cv2.VideoCapture(index)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('auth.signup'), code=302)

@main.route('/videofeed')
@login_required
def videofeed():
    return Response(gen(VideoCamera(0)),
                   mimetype='multipart/x-mixed-replace; boundary=frame')
