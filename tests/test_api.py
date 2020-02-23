import sys
import os
import conftest  # noqa: F401
import config
import worker
from unittest.mock import MagicMock
from time import sleep

sys.path.append('./src')


def test_twitter_api():
    if config.Config.TWITTER_API_KEY is None:
        assert True
        return
    from twitter_handler import get_tweets
    tweets = get_tweets('elonmusk')
    assert tweets is not None


def test_download_image():
    from twitter_handler import download_image
    # We test the download function by downloading an image and comparing it to a pre-downloaded image
    image = download_image('http://placehold.it/120x120&text=image1')
    with open('./tests/test_image.png', 'rb') as f:
        control_image = f.read()
    assert image == control_image


def test_tweet_to_image():
    if config.Config.TWITTER_API_KEY is None:
        assert True
        return
    from twitter_handler import get_tweets, tweet_to_image
    tweets = get_tweets('elonmusk')
    assert tweets is not None
    img_path = "./images/test_image"
    tweet_to_image(tweets[0], img_path)
    assert os.path.exists(img_path+'.png')


def test_queue_video(app):
    worker.create_twitter_video = MagicMock(side_effect=worker.create_twitter_video)
    worker.get_tweets = MagicMock(return_value=[])
    worker.convert_images_to_video = MagicMock(return_value="mocked")

    res = app.get("/video?user=elonmusk")
    sleep(1)  # wait for the worker to dispatch request
    assert res.status_code == 200
    assert worker.create_twitter_video.called


def test_video_progress(app):
    worker.create_twitter_video = MagicMock(side_effect=worker.create_twitter_video)
    worker.get_tweets = MagicMock(return_value=[])
    worker.convert_images_to_video = MagicMock(return_value="mocked")

    res = app.get("/video?user=elonmusk")
    progress = app.get(f"/progress/{res.json['video_id']}")
    sleep(1)  # wait for the worker to dispatch request
    assert res.status_code == 200
    assert progress.status_code == 200
    assert progress.json['status'] == "In queue" and progress.json['finished'] is False
    assert worker.create_twitter_video.called
    progress = app.get(f"/progress/{res.json['video_id']}")
    assert progress.json['status'] == "Video finished!" and progress.json['finished'] is True
