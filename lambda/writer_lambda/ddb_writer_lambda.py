import json
import csv
import boto3
import os

# This Lambda is triggered with the SQS.

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, contex):
    sqs_queue_url = os.environ.get("ENV_SQS_QUEUE")
    region_name = os.environ.get("ENV_REGION_NAME")
    print("Initiating Lambda")
    sqs = boto3.client("sqs", region_name=region_name)

    no_of_records = len(event["Records"])
    print(f"{no_of_records} files have been found in the bucket.")

    if "Records" in event:
        for rec in event["Records"]:
            print("Processing {}...".format(rec["messageId"]))
            receipt_handle = rec["receiptHandle"]
            body = rec["body"]
            ctr = json.loads(body)
            res = save_item_ddb(table, ctr)
            print("Customer ddb response: ", res)

            if res["ResponseMetadata"]["HTTPStatusCode"] == 200:
                sqs.delete_message(QueueUrl=sqs_queue_url, ReceiptHandle=receipt_handle)
                print("Message {} erased".format(rec["messageId"]))

    print("\n---End of Execution---\n")

    return 0


def save_item_ddb(table, item):
    response = table.put_item(Item=item)
    return response
