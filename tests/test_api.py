import sys
import os
# import pytest

sys.path.append('./src')


def test_twitter_api():
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
    from twitter_handler import get_tweets, tweet_to_image
    tweets = get_tweets('elonmusk')
    assert tweets is not None
    img_path = "./images/test_image"
    tweet_to_image(tweets[0], img_path)
    assert os.path.exists(img_path+'.png')
