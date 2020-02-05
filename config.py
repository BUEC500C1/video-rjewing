import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    TWITTER_API_KEY = os.getenv('EC500_TWITTER_API_KEY')
    TWITTER_SECRET_KEY = os.getenv('EC500_TWITTER_SECRET_KEY')
    TWITTER_ACCESS_TOKEN = os.getenv('EC500_TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_SECRET = os.getenv('EC500_TWITTER_ACCESS_SECRET')

    SECRET_KEY = os.getenv('EC500_SECRET_KEY', 'dev_key')

    # Set Host and Port
    API_IP = '0.0.0.0'
    API_PORT = 8080
