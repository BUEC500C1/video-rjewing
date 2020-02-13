import requests
from time import sleep


LOCAL_URL = "http://localhost:5000"
user = "elonmusk"

resp = requests.get(f"{LOCAL_URL}/video?user={user}")
resp_json = resp.json()
print(resp_json)

progress = requests.get(resp_json['url']).json()
print(progress)
while not progress['finished']:
    print(f"Task status: {progress['status']}")
    # DO WORK HERE
    sleep(1)
    progress = requests.get(resp_json['url']).json()

print("Video is ready!")
