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

On my laptop, I have 8 (4 physical + 4 virtual) cores (which is 800% CPU), so I should be able to run 2 of these operations at the same time without losing speed or throttling the conversion. If I go above this, then my computer will take longer to convert all the videos.

#### Task 2
1. Design a module that can queue and process videos and notify the caller when the videos are ready
2. Implement the model
3. Include tracking interface to show how many processes are going on and success of each

This task was accomplished using a Python multiproccessing ThreadPool object. The Python Pool library will manage a set of processes or threads for you and assign them tasks as requested to complete. Whenever an API call is made to the '/video' endpoint, a new task is added to the queue. A work dispatcher thread will pull tasks from this queue and assign it to the ThreadPool, which will spin up as many threads as are needed (up to the maximum specified) to process the task. The actual video conversion using ffmpeg is done through a subprocess, so the thread will not be slown down by the heavy CPU work required by ffmpeg.

The flow looks a little like this:
```
/video?user=elonmusk -> Task queued -> Task dequeued by work dispatcher ->
Task assigned to ThreadPool -> ThreadPool thread creates video -> Progress for video is updated
-> Video available on /display/VIDEO_ID
```

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
4. Run the command: `python3 app.py`
5. To test the API, run `curl localhost:5000/video?user=elonmusk`
6. Go to the URL provided when the video finishes after ~5 seconds.

## Docker
Alternatively, we can use docker-compose to easily deploy the application. First create the docker secret files as described in `docker/secrets/SECRETS.md`.

Then run `docker-compose -f "docker-compose.yml" up -d --build`.


### Setup email capabilities
To set up email, we need to defined the environment variables EC500_GMAIL_EMAIL and EC500_GMAIL_PASSWORD. We also need to allow "Less Secure Apps" to access the GMail account you are using. Go to [this link](https://myaccount.google.com/u/3/lesssecureapps?pageId=none) and ensure the *Allow less secure apps* setting is *ON*. An email will then be sent from this account when the video finishes if the user requests it.

## How To Use
### /video
We can test the api by running:
```
curl localhost:5000/video?user=elonmusk
```
This will return a json object with a message letting you know that the video has been queued for processing and a URL to view the video which will be available when it finishes. 

### /progress
We can check the progress of the video on the "/progress" endpoint, which will tell us what step of the task it is on and when it finishes. The response looks as follows, where VIDEO_ID is the video UUID:
```
{
    "video_id": VIDEO_ID,
    "status": "In queue",
    "finished": False
}
```
The status is changed as the video is processed to the current stage of the task. The finished variable is set to True when the video is finished.

You can see an example of this in the "./tests/example_app.py" file:
```
$ python3 ./tests/example_app.py

{'response': 'Created video named elonmusk-c8ebd6e5ae16409cbec997943e59abf0.ogg.', 'url': 'http://127.0.0.1:5000/progress/elonmusk-c8ebd6e5ae16409cbec997943e59abf0'}
{'video_id': 'elonmusk-c8ebd6e5ae16409cbec997943e59abf0', 'status': "Generating images from elonmusk's tweets", 'finished': False}
Task status: Generating images from elonmusk's tweets
Task status: Generating images from elonmusk's tweets
Task status: Generating images from elonmusk's tweets
Task status: Creating video from tweets
Video is ready!
```

### Video encoding
By default, the video is encoded into the 'OGG' video file format because it is supported by all browsers. However, we can specify a different encoding by passing the "format" parameter:
```
curl localhost:5000/video?user=elonmusk&format=mp4
```
This will encode the video into an MP4 video instead of an OGG video.

### Email
The API can also send an email once the video is finished by adding the "email" parameter:
```
curl localhost:5000/video?user=elonmusk&email=rjewing@bu.edu
```
This will send an email to rjewing@bu.edu when the video finishes.

## Explanation
The API call queues up a task to convert the Twitter user's timeline into a video. A worker running on a seperate thread pulls tasks from this queue and begins the tweet to video conversion. We can configure the number of workers with the NUM_WORKERS config variable.

First the worker pulls the user's timeline and extracts the necessary information from the tweets. It then generates an image for each tweet using the Pillow library. These images are then converted to a video using ffmpeg where each tweet is shown for 3 seconds.

When the video is finished, the video becomes available under the /display/VIDEO_ID path. Additionally, the finished variable from the progress report is set to True. Finally, if an email was provided in the request, the worker sends an email with the link to view the video to the user.

## Additional Features
### Workers
Each worker runs in it's own directory, so we can simply add additional workers if we have a lot of traffic. These workers will work independently of each other and maintain their own working directory with no extra work needed from the developer. We use threads for the workers, but dispatch a new process to perform the ffmpeg video conversion using python's builtin subprocess module. This way, we can share variables between the workers to make it easier to update progress, but enjoy better speed when performing the CPU bound task of converting the images to a video.


