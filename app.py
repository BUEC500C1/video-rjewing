from config import Config
import sys
sys.path.insert(0, "./src")

from api import app  # noqa: E402

if __name__ == '__main__':
    app.run(host=Config.API_IP, port=Config.API_PORT)
