import os
import pandas as pd

FEEDBACK_FILE = "feedback/feedback.csv"


def should_trigger_retraining(threshold: int = 10) -> bool:
    if not os.path.exists(FEEDBACK_FILE):
        return False

    df = pd.read_csv(FEEDBACK_FILE)

    negative_feedback = df[df["rating"].str.lower() == "negative"]

    return len(negative_feedback) >= threshold


if __name__ == "__main__":
    if should_trigger_retraining():
        print("Retraining trigger activated: feedback threshold reached.")
    else:
        print("Retraining not required yet.")
