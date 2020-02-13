import os
import uuid
from datetime import datetime
from multiprocessing import current_process, Queue
from shutil import rmtree
import threading
from subprocess import Popen
from twitter_handler import get_tweets, tweet_to_image
from gmail_handler import send_email

basedir = os.path.dirname(os.path.dirname(__file__))

work_queue = Queue()
work_progress = {}


def work_dispatcher(process_pool):
    while True:
        video_id, user, email, fmt = work_queue.get()
        print("Got work")
        print(work_progress)
        process_pool.apply_async(create_twitter_video, args=(video_id, user, email), kwds={'format': fmt})


def create_twitter_video(video_id, user, email, format='ogg'):
    print("Creating video")
    print(work_progress)
    work_progress[video_id]['status'] = f"Generating images from {user}'s tweets"
    image_path = os.path.join(basedir, 'images', uuid.uuid4().hex)
    os.mkdir(image_path)

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
    work_progress[video_id]['status'] = "Creating video from tweets"

    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "panic",
           "-f", "image2", "-i", f"{image_path}/tweet%d.png",
           "-preset", "ultrafast",
           "-r", "1/3", "-y", f"./videos/{video_id}.ogg"]

    p = Popen(cmd)
    p.communicate()

    rmtree(image_path)

    if email is not None:
        print(f"Sending email... {email}")
        send_email(email, video_id)

    work_progress[video_id]['status'] = f"Video finished!"
    work_progress[video_id]['finished'] = True
    print(f"{datetime.now()} -- Worker finished {video_id} for @{user}")

