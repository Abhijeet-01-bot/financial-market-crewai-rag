import os
import pandas as pd
from datetime import datetime

FEEDBACK_FILE = "feedback/feedback.csv"


def save_feedback(query, response, rating, comments=""):
    os.makedirs("feedback", exist_ok=True)

    record = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "response": response,
        "rating": rating,
        "comments": comments
    }

    if os.path.exists(FEEDBACK_FILE):
        df = pd.read_csv(FEEDBACK_FILE)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])

    df.to_csv(FEEDBACK_FILE, index=False)

    return True

