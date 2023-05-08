from keys import token
from config import api_url
import os
import json
import requests

#questions = os.listdir("questions/")

# Load state from previous day

with open("state.json", "r") as f:
    state = json.load(f)
    
post = True

# We only need to post if there was an answer in the file

if state["answer"] == "":
    post = False

# Generate message

cw = "The answer was " + state["answer"] + ". This post contains a list of people answering, might be long."

answerers = "People with correct answers were: "
for k, v in state["point_scorers"].items():
    answerers += "@" + str(k) + " (score: " + str(v) + "), "
    
next_question = str(int(state["today"].replace(".json", ""))+1) + ".json"
next_question = next_question.zfill(11)
print(next_question)

# Load next question for the state file and post

with open("questions/" + next_question, "r") as f:
    question = json.load(f)
    
if post:
    response = requests.post(
    url = api_url + "statuses/",
    headers={
        "Authorization": "Bearer " + token
    },
    json={"status": answerers, "visibility": "public", "spoiler_text": cw},
    )
    
    print(response.json())
    
# Generate new state file
    
new_day = question
new_day["current_hint"] = -1
new_day["today"] = next_question
new_day["latest_post"] = []
new_day["point_scorers"] = {}

with open("state.json", "w") as f:
    json.dump(new_day, f)

print(new_day)
