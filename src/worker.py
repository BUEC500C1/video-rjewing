from twitter_handler import get_tweets, tweet_to_image
from shutil import rmtree
from datetime import datetime
import os
import uuid

basedir = os.path.dirname(os.path.dirname(__file__))


def create_twitter_video(filename, user):
    image_path = os.path.join(basedir, 'images', uuid.uuid4().hex)
    os.mkdir(image_path)
    
    print(f"{datetime.now()} -- Worker making {filename} for @{user}")

    tweets = get_tweets(user)
    for n, tweet in enumerate(tweets):
        tweet_to_image(tweet, f"{image_path}/tweet{n}")

    os.system(
        f"ffmpeg -hide_banner -loglevel panic -f image2 -r 1/3 -i {image_path}/tweet%d.png -y ./videos/{filename}.ogg")
    rmtree(image_path)
    print(f"{datetime.now()} -- Worker finished {filename} for @{user}")

