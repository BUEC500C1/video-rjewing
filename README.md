# video-rjewing

## Answers to homework questions
#### Re-encoding Video Files
The commands I used to re-encode a video file to the two bitrates were:

**720p at 2Mbps and 30fps:**
```
ffmpeg -i input.mp4 -c:a copy -c:v copy -r 30 -s hd720 -b:v 2M output.mp4
```
**480p at 1Mbps and 30fps:**
```
ffmpeg -i input.mp4 -c:a copy -c:v copy -r 30 -s hd480 -b:v 1M output.mp4
```

#### Task 1
1. Estimate the processing power needed to execute such operations on your computer.
   
I ran the command to convert a video to 720p and found that it used ~400% CPU using the `top` command.

2. Estimate the maximum number of such operations that can run on your system.

On my laptop, I have 8 cores (800% CPU), so I should be able to run 2 of these operations at the same time without losing speed or throttling the convertion. If I go above this, then my computer will take longer to convert all the videos.

#### Task 2
1. Design a module that can queue and process videos and notify the caller when the videos are ready
2. Implement the model
3. Include tracking interface to show how many processes are going on and success of each

This task was accomplished using a Python multiproccessing Pool object. The Python Pool library will manage a set of processes for you and give them tasks as requested to complete.

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


