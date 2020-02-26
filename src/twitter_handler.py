import tweepy
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps
from textwrap import wrap
import sys
sys.path.insert(0, '..')
from config import Config  # noqa: E402

FONT_PATH = "./fonts/OpenSansEmoji.ttf"

auth = tweepy.OAuthHandler(Config.TWITTER_API_KEY, Config.TWITTER_SECRET_KEY)
auth.set_access_token(Config.TWITTER_ACCESS_TOKEN,
                      Config.TWITTER_ACCESS_SECRET)

api = tweepy.API(auth)


class Tweet():
    def __init__(self, username, name, profile_picture, text, time, images):
        self.username = '@' + username
        self.name = name
        self.profile_picture = profile_picture
        self.text = text
        self.time = time
        self.images = images

    def __repr__(self):
        return f'{{"user": {self.username}, "text": {self.text}, "media": {self.images}}}'

    def __str__(self):
        return f"{self.time} - @{self.username}: \"{self.text}\" -- Media: {self.images}"

    def to_json(self):
        return {"user": self.username, "text": self.text, "media": self.images}


def download_image(url):
    response = requests.get(url, stream=True)
    image_content = response.content
    return image_content


def get_tweets(username):
    timeline_statuses = api.user_timeline(username, tweet_mode='extended')
    tweets = []
    for tweet in timeline_statuses:
        images = []
        # collect all images
        if 'media' in tweet.entities:
            for media in tweet.extended_entities['media']:
                if media.get("type", None) == "photo":
                    images.append(media["media_url"])

        tweets.append(Tweet(
            tweet.user.screen_name,
            tweet.user.name,
            tweet.user.profile_image_url.replace(
                '_normal', ''),
            tweet.full_text,
            tweet.created_at,
            images))

    return tweets


def tweet_to_image(tweet, img_name):
    def crop_to_circle(crop_img):
        bigsize = (crop_img.size[0]*3, crop_img.size[1]*3)
        mask = Image.new('L', bigsize, 0)
        ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(crop_img.size, Image.ANTIALIAS)
        mask = ImageChops.darker(mask, crop_img.split()[-1])
        crop_img.putalpha(mask)
        return crop_img, mask

    FONT_USER_INFO = ImageFont.truetype(
        FONT_PATH, 70, encoding="utf-8")
    FONT_TEXT = ImageFont.truetype(
        FONT_PATH, 50, encoding="utf-8")
    RESOLUTION = (2376, 2024)
    COLOR_TEXT = 'black'
    COORD_PHOTO = (220, 160)
    COORD_NAME = (600, 185)
    COORD_TAG = (600, 305)
    COORD_TEXT = (250, 510)
    LINE_MARGIN = 15

    text_string_lines = wrap(tweet.text, 60)
    temp_img = Image.new('RGB', (0, 0))
    temp_img_draw_interf = ImageDraw.Draw(temp_img)
    line_height = [
        temp_img_draw_interf.textsize(text_string_lines[i], font=FONT_TEXT)[1]
        for i in range(len(text_string_lines))
    ]

    img = Image.new('RGB', RESOLUTION, color='white')
    drawing = ImageDraw.Draw(img)
    drawing.text(COORD_NAME, tweet.name or "unknown", font=FONT_USER_INFO, fill='black')
    drawing.text(COORD_TAG, tweet.username or "unknown", font=FONT_USER_INFO, fill='black')

    x = COORD_TEXT[0]
    y = COORD_TEXT[1]
    for index, line in enumerate(text_string_lines):
        # Draw a line of text
        drawing.text((x, y), line, font=FONT_TEXT, fill=COLOR_TEXT)
        # Increment y to draw the next line at the adequate height
        y += line_height[index] + LINE_MARGIN

    y += 50
    drawing.text((x, y), tweet.time.strftime("%m/%d/%Y %H:%M:%S"), font=FONT_TEXT, fill='gray')
    y += line_height[index] + LINE_MARGIN

    if tweet.profile_picture is not None:
        user_photo_bytes = download_image(tweet.profile_picture)
        # user_photo = Image.frombuffer('RGB', (48, 48), user_photo_bytes, decoder_name='jpeg')
        user_photo = Image.open(BytesIO(user_photo_bytes)).convert(
            'RGBA').resize((300, 300))
        user_photo, mask = crop_to_circle(user_photo)
        img.paste(user_photo, COORD_PHOTO, mask)

    old_y = y
    for url in tweet.images:
        tweet_img_bytes = download_image(url)
        tweet_img = Image.open(BytesIO(tweet_img_bytes)).convert('RGBA')
        tweet_img.thumbnail((800, 800), Image.ANTIALIAS)
        tweet_img = ImageOps.expand(tweet_img, border=2)

        if y + tweet_img.size[1] > RESOLUTION[1]:
            y = old_y
            x += tweet_img.size[0] + LINE_MARGIN
        img.paste(tweet_img, (x, y))

        y += tweet_img.size[1] + LINE_MARGIN

    img.save(f'{img_name}.png', format='png')
    return img_name


if __name__ == '__main__':
    FONT_PATH = "../fonts/OpenSansEmoji.ttf"
    # print(api.get_status('1222679152819494913', tweet_mode='extended').__dict__)
    for t in get_tweets('elonmusk'):
        tweet_to_image(t, 'test')
