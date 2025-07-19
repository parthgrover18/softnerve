import json
import os
import numpy as np
from collections import defaultdict

REWARD_HISTORY_FILE = "data/rewards/history.log"

def load_rewards(log_file=REWARD_HISTORY_FILE):
    rewards = []
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            for line in f:
                try:
                    rewards.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return rewards

def build_q_table(rewards):
    q_table = defaultdict(lambda: 0.0)
    for entry in rewards:
        state = entry.get("chapter")
        action = f"version_{entry.get('timestamp')}"
        reward = entry.get("reward", 0.0)
        q_table[(state, action)] += reward
    return q_table

def best_version_for_chapter(q_table, chapter):
    best_version = None
    highest_score = float("-inf")

    for (state, action), score in q_table.items():
        if state == chapter and score > highest_score:
            highest_score = score
            best_version = action

    if best_version is None:
        return None
    return best_version, highest_score

def suggest_action(q_table):
    if not q_table:
        return "explore"
    values = list(q_table.values())
    avg = np.mean(values)
    if avg > 12:
        return "exploit"
    elif avg < 6:
        return "explore"
    return "balance"
