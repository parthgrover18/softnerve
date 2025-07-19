import chromadb
import json

client = chromadb.PersistentClient(path="data/chroma_db")

collection = client.get_or_create_collection(name="chapter_versions")


def append_reward_to_log(log_file_path):

    with open(log_file_path, "r") as f:
        lines = f.readlines()
        if not lines:
            print("Log file is empty.")
            return
        last_line = lines[-1].strip()

    try:
        entry_dict = json.loads(last_line)
    except json.JSONDecodeError:
        print("Failed to decode the last log entry.")
        return

    text = entry_dict.pop("text", None)


    doc_id = f"{entry_dict.get('chapter', 'unknown')}_{entry_dict.get('timestamp', 'unknown')}"

    collection.add(
        documents=[text],
        metadatas=[entry_dict],
        ids=[doc_id]
    )

def print_max_reward_text():
    results = collection.get()
    if not results["documents"]:
        print("No documents found in the database.")
        return

    max_reward = float("-inf")
    max_text = None

    for text, metadata in zip(results["documents"], results["metadatas"]):
        reward = metadata.get("reward", 0)
        if reward > max_reward:
            max_reward = reward
            max_text = text

    if max_text:
        print(f"Maximum reward: {max_reward}")
        print("Text with the maximum reward:")
        print(max_text)
    else:
        print("No valid reward found in documents.")

