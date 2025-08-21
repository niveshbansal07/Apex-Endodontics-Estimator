# tracking_utils.py
import csv
from datetime import datetime
import os

def log_submission(data, estimate_value):
    os.makedirs("logs", exist_ok=True)
    with open("logs/estimate_log.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.get("full_name"),
            data.get("email"),
            data.get("phone"),
            data.get("treatment"),
            data.get("tooth"),
            estimate_value
        ])
