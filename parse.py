from keys import token
from config import api_url
import json
import requests
import sys

scores = {
    0: 5,
    1: 4,
    2: 3,
    3: 2,
    4: 1,
    }

cw = ""

#api_url = ""

def get_context(post, api_url):
    response = requests.get(
    url= api_url + "statuses/" + post + "/context",
    headers={
        "Authorization": "Bearer " + token
    },
    )
    return response.json()["descendants"]

# Load the state of the game file

with open("state.json", "r") as f:
    state = json.load(f)
    
if state["today"] == "" or state["question"] == "":
    sys.exit()
    
check_answers = False

# Check how many hints we've used up today and form the message based on that

if state["current_hint"] == -1:
    msg = "Today's question is: " + state["question"]
elif 0 <= state["current_hint"] < len(state["hints"]):
    cw = "Hint about today's question;  reply to this post if you want to give an answer now"
    hints = "Previous hints:\n"
    i = 1
    for hint in state["hints"]:
        if i <= state["current_hint"]:
            hint += "- " +  hint + "\n"
        i += 1
    msg = "Hint: " + state["hints"][state["current_hint"]]
    msg += "\nToday's question: \"" + state["question"] + "\""
    
    msg += "\nNew correct answers by: "
    check_answers = True
else:
    hints = "Hints:\n"
    for hint in state["hints"]:
        hints += "- " +  hint + "\n"
    cw = "2 hourly update about today's question; reply to this post if you want to give an answer now"
    msg = "Today's question: \"" + state["question"] + "\" \n" + hints + "New correct answers by: "
    check_answers = True

# Check if there are answers on the latest post
        
if check_answers:
    latest_correct = []
    point_scorers = state["point_scorers"]
    descendants = get_context(state["latest_post"][-1], api_url)
    for reply in descendants:
        if state["answer"].lower().replace(" ", "") in reply["content"].lower().replace(" ", "") and state["answer"] != "":
            if state["current_hint"] in scores.keys():
                point_scorers[reply["account"]["acct"]] = scores[state["current_hint"]]
            else:
                point_scorers[reply["account"]["acct"]] = 1
            latest_correct.append(reply["account"]["acct"])
    for acct in latest_correct:
        msg += "@" + acct + ", "
    if len(latest_correct) == 0:
        msg += "none"
    point_scorers = dict(sorted(point_scorers.items(), key=lambda item: item[1], reverse=True))
    state["point_scorers"] = point_scorers

# Send post to server

response = requests.post(
url = api_url + "statuses/",
headers={
    "Authorization": "Bearer " + token
},
json={"status": msg, "visibility": "public", "spoiler_text": cw},
)
print(response)
print(response.content)
state["latest_post"].append(response.json()["id"])
    
# Handle updated state file
    
state["current_hint"] += 1
        
with open("state.json", "w") as f:
    json.dump(state, f)
