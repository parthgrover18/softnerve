import json
import os
from datetime import datetime

def log_reward(chapter_name, reward, feedback, text):
    log_path = "data/rewards/history.log"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "timestamp": timestamp,
        "chapter": chapter_name,
        "reward": reward,
        "score": feedback.get("score"),
        "AI_score":feedback.get("AI_score"),
        "approved": feedback.get("approved"),
        "tone_ok": feedback.get("tone_ok"),
        "recommend": feedback.get("recommend_for_publishing"),
        "text": text
    }
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")
        print('entry saved to data/rewards/history.log')

def calculate_reward(feedback_json_path, text):

    try:
        with open(feedback_json_path, 'r') as f:
            feedback_list = json.load(f)
    except:
        return 0.0

    if not hasattr(feedback_list, 'append') or len(feedback_list) == 0:
        return 0.0

    latest = feedback_list[-1]

    reward = (latest.get("score")+latest.get("AI_score"))/2

    if latest.get("approved"):
        reward += 2.0
    else:
        -2.0
    
    if latest.get("tone_ok"):
        reward += 1.0  
    else:
        -1.0

    if latest.get("recommend_for_publishing"):
        reward += 3.0  
    else:
        0

    chapter_name = os.path.splitext(os.path.basename(feedback_json_path))[0]
    log_reward(chapter_name, reward, latest, text)

    print(f"Calculated reward: {round(reward, 2)}")
    return round(reward, 2)
