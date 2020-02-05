import os
import sys
import shutil
import atexit

import resources

from time import sleep
from queue import Queue
from flask import Flask, url_for, send_from_directory
from flask_restful import Api

from worker import VideoWorker
from config import Config

basedir = os.path.dirname(os.path.dirname(__file__))
image_dir = os.path.join(basedir, 'images')
video_dir = os.path.join(basedir, 'videos')
# rebuild image directory
shutil.rmtree(image_dir)
os.mkdir(image_dir)
# create video directory if not exists
if not os.path.exists(video_dir):
    os.mkdir(video_dir)


app = Flask(__name__)
app.config.from_object(Config)

q = Queue()

api = Api(app)
api.add_resource(resources.TwitterSummarizer, '/video',
                 resource_class_kwargs={'q': q})

workers = []
for _ in range(1):
    workers.append(VideoWorker(q))
    workers[-1].start()


@app.route('/display/<video_id>')
def video_displayer(video_id):
    video_name = f"{video_id}.ogg"
    html = f"""
        <video width="1280" height="720" controls>
            <source src="{url_for('video_feed', video_id=video_name)}" type="video/ogg">
            Your browser does not support the video tag.
        </video>
    """
    return html, 200


@app.route('/video/<video_id>')
def video_feed(video_id):
    return send_from_directory(os.path.abspath(os.path.join(basedir, 'videos')), video_id, mimetype='video/ogg')


def exit_handler():
    print('Shutting down server...')
    for w in workers:
        w.stop()
    sleep(0.5)
    sys.exit(0)


atexit.register(exit_handler)

if __name__ == '__main__':
    app.run()
