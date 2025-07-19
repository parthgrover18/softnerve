import json
import os
from datetime import datetime

def load_text(path):
    with open(path, 'r') as f:
        return f.read()

def get_feedback():
    while True:
        decision = input("Approve this version? (y/n): ").lower()
        if decision in ['y', 'n']:
            break
    approved = decision == 'y'

    while True:
        try:
            score = int(input("Give a score (1-10): "))
            if 1 <= score <= 10:
                break
            else:
                print("Score must be between 1 and 10.")
        except ValueError:
            print("Please enter a valid integer.")

    comment = input("Optional comment: ")

    while True:
        tone_response = input("Was the tone appropriate for the original text? (y/n): ").lower()
        if tone_response in ['y', 'n']:
            tone_ok = tone_response == 'y'
            break
        else:
            print("Please enter 'y' or 'n'.")

    while True:
        publish_response = input("Would you recommend this version for publishing? (y/n): ").lower()
        if publish_response in ['y', 'n']:
            publishable = publish_response == 'y'
            break
        else:
            print("Please enter 'y' or 'n'.")

    return approved, score, comment, tone_ok, publishable

def display(rating):
    raw_path = "data/raw/chapter1.txt"
    reviewed_path = "data/processed/chapter1_reviewed.txt"
    feedback_path = "data/feedback/chapter1_feedback.json"

    print("\nComparing Texts (showing both texts one by one):\n")

    raw_text = load_text(raw_path)
    reviewed_text = load_text(reviewed_path)

    print("\n\nOriginal Text:\n\n\n", raw_text,'\n\n\n\n\n')
    print("\n\nAI Reviewed Text:\n\n\n", reviewed_text,'\n\n\n\n\n')

    approved, score, comment, tone_ok, publishable = get_feedback()

    feedback_entry = {
        "chapter": "chapter1",
        "approved": approved,
        "score": score,
        "comments": comment,
        "tone_ok": tone_ok,
        "recommend_for_publishing": publishable,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "AI_score": rating
    }

    os.makedirs(os.path.dirname(feedback_path), exist_ok=True)

    if os.path.exists(feedback_path):
        with open(feedback_path, 'r') as f:
            try:
                data = json.load(f)
                if hasattr(data, 'append'):
                    feedback_list = data
                else:
                    feedback_list = [data]
            except json.JSONDecodeError:
                feedback_list = []
    else:
        feedback_list = []

    feedback_list.append(feedback_entry)

    with open(feedback_path, 'w') as f:
        json.dump(feedback_list, f, indent=2)

    print(f"\nFeedback saved to {feedback_path}")


