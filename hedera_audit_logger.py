import csv
from hedera import (
    Client, PrivateKey, AccountId, TopicCreateTransaction, TopicMessageSubmitTransaction
)

ACCOUNT_ID = "0.0.7147612"
PRIVATE_KEY = "3030020100300706052b8104000a042204202c5dd63d616ecd95a9ff3f4aff9b57ecc4645a3ae518bfc7dffb7e8c459f70c5"
client = Client.forTestnet()
client.setOperator(AccountId.fromString(ACCOUNT_ID), PrivateKey.fromString(PRIVATE_KEY))

def log_to_hedera(message):
    tx = TopicMessageSubmitTransaction().setTopicId(topic_id).setMessage(message)
    tx.execute(client)

topic_tx = TopicCreateTransaction().execute(client)
topic_receipt = topic_tx.getReceipt(client)
topic_id = topic_receipt.topicId

print("Created topic:", topic_id)
print("Created topic ID:", topic_id.toString())

with open("data.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        message = f"{row['Date']} - {row['Event']} - {row['Details']}"
        tx = TopicMessageSubmitTransaction().setTopicId(topic_id).setMessage(message).execute(client)
        print("Logged:", message)
