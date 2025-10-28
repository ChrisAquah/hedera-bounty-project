# analyze_and_publish.py
# Reads data.csv, prints a simple summary, and posts the summary to a Hedera topic.
import pandas as pd
from hedera import Client, AccountId, PrivateKey, TopicMessageSubmitTransaction


ACCOUNT_ID = "0.0.7147612"
PRIVATE_KEY = "3030020100300706052b8104000a042204202c5dd63d616ecd95a9ff3f4aff9b57ecc4645a3ae518bfc7dffb7e8c459f70c5"

# Connect to Hedera testnet
client = Client.forTestnet()
client.setOperator(AccountId.fromString(ACCOUNT_ID), PrivateKey.fromString(PRIVATE_KEY))

# Load CSV
df = pd.read_csv("data.csv")

# Simple analytics
total_rows = len(df)
unique_events = df["Event"].nunique() if "Event" in df.columns else "N/A"
top_event = df["Event"].value_counts().idxmax() if "Event" in df.columns and total_rows>0 else "N/A"

summary_lines = [
    f"Total rows: {total_rows}",
    f"Unique events: {unique_events}",
    f"Most common event: {top_event}"
]
summary_text = " | ".join(summary_lines)

print("ANALYTICS SUMMARY")
for line in summary_lines:
    print(line)

# Ask user for topic id to publish summary
topic_input = input("Enter Hedera topic ID to publish summary (or type 'skip'): ").strip()

from hedera import TopicId
if topic_input.lower() != "skip" and topic_input != "":
    topic_input = TopicId.fromString(topic_input)
    tx = TopicMessageSubmitTransaction().setTopicId(topic_input).setMessage(summary_text).execute(client)
    print("Published summary to topic:", topic_input)
else:
    print("Skipped publishing to Hedera topic.")
