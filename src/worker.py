import os
import threading
import uuid
from datetime import datetime
from multiprocessing import Queue, current_process
from shutil import rmtree
from subprocess import Popen

from gmail_handler import send_email
from twitter_handler import get_tweets, tweet_to_image

basedir = os.path.dirname(os.path.dirname(__file__))

work_queue = Queue()
work_progress = {}


def update_work_progress(video_id, key=None, val=None):
    if video_id not in work_progress:
        work_progress[video_id] = {
            "video_id": video_id,
            "status": "",
            "finished": False
        }
    if key is None:
        return
    work_progress[video_id][key] = val


def work_dispatcher(process_pool):
    while True:
        video_id, user, email, fmt = work_queue.get()
        print("Got work")
        process_pool.apply_async(create_twitter_video, args=(video_id, user, email), kwds={'format': fmt})


def create_twitter_video(video_id, user, email, format='ogg'):
    print("Creating video")
    update_work_progress(video_id, key='status', val=f"Generating images from {user}'s tweets")
    image_path = create_image_dir()

    print(f"{datetime.now()} -- Worker ({current_process()}) making {video_id} for @{user}")

    tweets = get_tweets(user)
    threads = []
    for n, tweet in enumerate(tweets):
        t = threading.Thread(target=tweet_to_image, args=(
            tweet, f"{image_path}/tweet{n}"))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print('Finished making images...')
    update_work_progress(video_id, key='status', val="Creating video from tweets")

    convert_images_to_video(image_path, video_id)

    rmtree(image_path)

    if email is not None:
        print(f"Sending email... {email}")
        send_email(email, video_id)

    update_work_progress(video_id, key='status', val=f"Video finished!")
    update_work_progress(video_id, key='finished', val=True)
    print(f"{datetime.now()} -- Worker finished {video_id} for @{user}")


def create_image_dir():
    image_path = os.path.join(basedir, 'images', uuid.uuid4().hex)
    os.mkdir(image_path)
    return image_path


def convert_images_to_video(image_path, video_id):
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "panic",
           "-f", "image2", "-i", f"{image_path}/tweet%d.png",
           "-preset", "ultrafast",
           "-r", "1/3", "-y", f"./videos/{video_id}.ogg"]
    p = Popen(cmd)
    p.communicate()
