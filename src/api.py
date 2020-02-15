import os
import sys
import shutil
import resources
import signal
from time import sleep
from multiprocessing.pool import ThreadPool
from flask import Flask, url_for, send_from_directory
from flask_restful import Api
from config import Config
from threading import Thread
from worker import work_dispatcher

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

# Make threads/processes ignore sigint for clean exit
signal.signal(signal.SIGINT, signal.SIG_IGN)
process_pool = ThreadPool(Config.NUM_WORKERS)

# initialize api endpoints
api = Api(app)
api.add_resource(resources.TwitterSummarizer, '/video')
api.add_resource(resources.VideoProgress, '/progress/<string:video_id>')

# initialize work dispatcher
queue_handler_thread = Thread(target=work_dispatcher, daemon=True, args=(process_pool,))
queue_handler_thread.start()


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


def exit_handler(*args, **kwargs):
    print('Shutting down server...')
    process_pool.terminate()
    process_pool.join()

    sleep(1)
    sys.exit(0)


signal.signal(signal.SIGTERM, exit_handler)
signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGQUIT, exit_handler)

if __name__ == '__main__':
    app.run()
