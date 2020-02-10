import os
import uuid
from datetime import datetime
from multiprocessing import current_process
from shutil import rmtree
import ffmpeg

from twitter_handler import get_tweets, tweet_to_image

basedir = os.path.dirname(os.path.dirname(__file__))


def create_twitter_video(filename, user, format='ogg'):
    image_path = os.path.join(basedir, 'images', uuid.uuid4().hex)
    os.mkdir(image_path)

    print(f"{datetime.now()} -- Worker ({current_process()}) making {filename} for @{user}")

    tweets = get_tweets(user)
    for n, tweet in enumerate(tweets):
        tweet_to_image(tweet, f"{image_path}/tweet{n}")

    video = ffmpeg.input(f"{image_path}/tweet%d.png", f="image2", r="1/3", loglevel="quiet")
    video = ffmpeg.output(video, f"./videos/{filename}.{format}")
    video = ffmpeg.overwrite_output(video)
    ffmpeg.run(video)

    rmtree(image_path)
    print(f"{datetime.now()} -- Worker finished {filename} for @{user}")
