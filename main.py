import os
from dotenv import load_dotenv
from scraping.scraper import scrape_chapter
from utils.logger import get_logger
from agents.ai_writer import spin_text
from agents.ai_reviewer import review_text
from agents.human_interface import display
from scraping.screenshotter import capture_scrolled_screenshots
from agents.reward_engine import calculate_reward
from rl_model.rl_reward_system import *
from agents.database import *

load_dotenv()

logger = get_logger("main")

def main():
    try:
        logger.info("Starting softnerve pipeline...")

        # Step 1: Scrape raw chapter
        url = os.getenv('URL')
        scrape_chapter(url)
        logger.info("Scraping complete.")

        # Step 2: Screenshotting the webpage
        capture_scrolled_screenshots(url)
        logger.info("Screenshots captured.")

        # Step 3: AI Writer spins the cleaned text
        api_key = os.getenv('API_KEY')
        spin_text("data/raw/chapter1.txt", "data/processed/chapter1_writer.txt",api_key)
        logger.info("AI writer completed.")

        # Step 4: AI Reviewer improves the spun text
        (rating, final_text)=review_text("data/processed/chapter1_writer.txt", "data/processed/chapter1_reviewed.txt",api_key)
        logger.info("AI reviewer completed.")

        # Step 5: Human-in-the-loop interface for feedback
        display(rating)
        logger.info("Human feedback collected and stored.")

        # Step 6: Reward engine calculates the reward from given feedback out of 10
        calculate_reward("data/feedback/chapter1_feedback.json", final_text)
        logger.info("Reward calculated and stored.")

        # Step 7: Finds Strategy Suggestion and best version of chapter using Reinforcement Learning
        rewards = load_rewards()
        q_table = build_q_table(rewards)
        strategy = suggest_action(q_table)
        logger.info(f"RL-Based Strategy Suggestion: {strategy}")

        # Step 8: Store the most recent reward entry from history.log into ChromaDB and print the top scoring text
        append_reward_to_log("data/rewards/history.log")
        logger.info("Latest reward entry stored in ChromaDB.")

        logger.info("Retrieving document with highest reward from ChromaDB...")
        print_max_reward_text()


        logger.info("Pipeline finished successfully.")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")


main()