# video-rjewing

## Setup

1. `pip3 install -r requirements.txt`
2. Export the environment variables with the proper values:
```
EC500_TWITTER_API_KEY=XXXXXX
EC500_TWITTER_SECRET_KEY=XXXXXX
EC500_TWITTER_ACCESS_TOKEN=XXXXXX
EC500_TWITTER_ACCESS_SECRET=XXXXXX
```
3. Install ffmpeg from ```https://www.ffmpeg.org/download.html```
4. Run the command: `flask run`
5. To test the API, run `curl localhost:5000/video?user=elonmusk`
6. Go to the URL provided when the API call returns.

## Docker
Alternatively, we can use docker-compose to easily deploy the application. First create the docker secret files as described in `docker/secrets/SECRETS.md`.

Then run `docker-compose -f "video-rjewing/docker-compose.yml" up -d --build`.

## Explanation
The API call queues up a task to convert the Twitter user's timeline into a video. A worker running on a seperate thread pulls tasks from this queue and begins the tweet to video conversion.

First the worker pulls the user's timeline and extracts the necessary information from the tweets. It then generates an image for each tweet using the Pillow library. These images are then converted to a video using ffmpeg where each tweet is shown for 3 seconds.

When the video is finished, the API call returns and sends back a link with the video ID so the user can view it.

## Additional Features
### Workers
Each worker runs in it's own directory, so we can simply add additional workers if we have a lot of traffic. These workers will work independently of each other and maintain their own working directory with no extra work needed from the developer.


