from threading import Thread
from twitter_handler import get_tweets, tweet_to_image
import os
import uuid


def remove_image_files(image_dir):
    filelist = [f for f in os.listdir(image_dir) if f.endswith(".png")]
    for f in filelist:
        os.remove(os.path.join(image_dir, f))


class VideoWorker(Thread):
    def __init__(self, q):
        Thread.__init__(self)
        self.running = True
        self.q = q

        basedir = os.path.dirname(os.path.dirname(__file__))
        self.image_path = os.path.join(basedir, 'images', uuid.uuid4().hex)
        os.mkdir(self.image_path)

        print("Worker intialized!")

    def run(self):
        while self.running:
            filename, user = self.q.get()
            print(f"Worker making {filename} for @{user}")

            remove_image_files(self.image_path)  # clear out old images
            tweets = get_tweets(user)
            for n, tweet in enumerate(tweets):
                tweet_to_image(tweet, f"{self.image_path}/tweet{n}")

            os.system(
                f"ffmpeg -hide_banner -loglevel panic -f image2 -r 1/3 -i {self.image_path}/tweet%d.png -y ./videos/{filename}.ogg")
            self.q.task_done()

    def stop(self):
        self.running = False
