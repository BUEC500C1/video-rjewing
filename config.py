import os

basedir = os.path.abspath(os.path.dirname(__file__))


def load_secret_from_path(name: str) -> str:
    path = f"/run/secrets/{name}"
    if not os.path.exists(path):
        return None

    with open(path, "r") as secret_file:
        return secret_file.read().strip()


class Config():
    TWITTER_API_KEY = load_secret_from_path('EC500_TWITTER_API_KEY') or os.getenv('EC500_TWITTER_API_KEY')
    TWITTER_SECRET_KEY = load_secret_from_path('EC500_TWITTER_SECRET_KEY') or os.getenv('EC500_TWITTER_SECRET_KEY')
    TWITTER_ACCESS_TOKEN = load_secret_from_path('EC500_TWITTER_ACCESS_TOKEN') or os.getenv('EC500_TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_SECRET = load_secret_from_path('EC500_TWITTER_ACCESS_SECRET') or os.getenv('EC500_TWITTER_ACCESS_SECRET')

    SECRET_KEY = load_secret_from_path('EC500_SECRET_KEY') or os.getenv('EC500_SECRET_KEY', 'dev_key')

    # Set Host and Port
    API_IP = '0.0.0.0'
    API_PORT = 5000

    GMAIL_EMAIL = load_secret_from_path('EC500_GMAIL_EMAIL') or os.getenv('EC500_GMAIL_EMAIL')
    GMAIL_PASSWORD = load_secret_from_path('EC500_GMAIL_PASSWORD') or os.getenv('EC500_GMAIL_PASSWORD')
