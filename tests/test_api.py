import sys
import os
import conftest  # noqa: F401
import config
import worker
import twitter_handler
from unittest.mock import MagicMock
from time import sleep
from datetime import datetime

base_dir = os.path.dirname(os.path.dirname(__file__))

sys.path.append(f'{base_dir}/src')

fake_tweets = [twitter_handler.Tweet(
    "elonmusk", "Elon Musk", None, "hello world!", datetime.now(), [])]
if config.Config.TWITTER_API_KEY is None:
    # Mock out all instances of get_tweets
    twitter_handler.get_tweets = MagicMock(return_value=fake_tweets)
    worker.get_tweets = MagicMock(return_value=fake_tweets)


def test_twitter_api():
    tweets = twitter_handler.get_tweets('elonmusk')
    assert tweets is not None


def test_download_image():
    # We test the download function by downloading an image and comparing it to a pre-downloaded image
    image = twitter_handler.download_image(
        'http://placehold.it/120x120&text=image1')
    with open(f'{base_dir}/tests/test_image.png', 'rb') as f:
        control_image = f.read()
    assert image == control_image


def test_tweet_to_image():
    tweets = twitter_handler.get_tweets('elonmusk')
    assert tweets is not None
    img_path = f"{base_dir}/images/test_image"
    twitter_handler.tweet_to_image(tweets[0], img_path)
    assert os.path.exists(img_path+'.png')


def test_create_twitter_video():
    orig_func = worker.get_tweets
    worker.get_tweets = MagicMock(return_value=fake_tweets)
    tweets = twitter_handler.get_tweets('elonmusk')
    assert tweets is not None

    worker.create_twitter_video('test-video', 'user', None)
    assert os.path.exists(f"{base_dir}/videos/test-video.ogg")
    worker.get_tweets = orig_func
    os.unlink(f"{base_dir}/videos/test-video.ogg")
    

def test_queue_video(app):
    orig_func = worker.create_twitter_video
    worker.create_twitter_video = MagicMock(return_value="mocked")

    res = app.get("/video?user=elonmusk")
    assert res.status_code == 200
    sleep(1)  # wait for the worker to dispatch request
    assert worker.create_twitter_video.called
    assert worker.work_queue.empty()
    worker.create_twitter_video = orig_func


def test_video_progress(app):
    worker.create_twitter_video = MagicMock(
        side_effect=worker.create_twitter_video)
    # worker.convert_images_to_video = MagicMock(return_value="mocked")
    res = app.get("/video?user=elonmusk")
    progress = app.get(f"/progress/{res.json['video_id']}")
    assert res.status_code == 200  # video request was successful
    assert progress.status_code == 200  # progress request was successful
    assert progress.json['status'] == "In queue" and progress.json['finished'] is False  # video is in queue and not finished

    # Wait for video to become finished
    while not progress.json['finished']:
        sleep(1)
        progress = app.get(f"/progress/{res.json['video_id']}")

    assert worker.create_twitter_video.called  # make sure the function was called
    progress = app.get(f"/progress/{res.json['video_id']}")
    assert progress.json['status'] == "Video finished!" and progress.json['finished'] is True  # make sure the video progress is set
    assert os.path.exists(f"{base_dir}/videos/{res.json['video_id']}.ogg")  # make sure the video exists
    os.unlink(f"{base_dir}/videos/{res.json['video_id']}.ogg")
