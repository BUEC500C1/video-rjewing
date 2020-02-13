import requests
from time import sleep


URL = "http://localhost:5000"
user = "elonmusk"

resp = requests.get(f"{URL}/video?user={user}")
resp_json = resp.json()
print(resp_json)

progress = requests.get(f"{URL}{resp_json['url']}").json()
print(progress)
while not progress['finished']:
    print(f"Task status: {progress['status']}")
    # DO WORK HERE
    sleep(1)
    progress = requests.get(f"{URL}{resp_json['url']}").json()

print("Video is ready!")
