import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

log_filename = datetime.now().strftime("logs/softnerve_%Y-%m-%d.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

def get_logger(name):
    return logging.getLogger(name)