import json
import csv
import boto3
import os
import s3

# This lambda is triggered by the Client S3 and sends to the WRITE queue.

PATH_PREFIX = "/tmp/"
CSV_SEPARATOR = ","


def lambda_handler(event, contex):
    no_of_records = len(event["Records"])
    print(f"{no_of_records} files have been found in the bucket.")

    sqs_queue_url = os.environ.get("ENV_SQS_QUEUE")
    region_name = os.environ.get("ENV_REGION_NAME")

    sqs = boto3.client("sqs", region_name=region_name)

    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        filename = key.split("/")[-1]
        s3.download_file(bucket, key, PATH_PREFIX, filename)
        csv_file_path = PATH_PREFIX + filename
        print(f"Started reading {csv_file_path}")

        with open(csv_file_path, encoding="utf-8") as csvf:
            csv_reader = csv.DictReader(csvf, delimiter=CSV_SEPARATOR)

            for rows in csv_reader:
                elem = json.loads(json.dumps(rows))
                print("** Sending msg", elem, "to the queue", sqs_queue_url)
                response = sqs.send_message(
                    QueueUrl=sqs_queue_url, MessageBody=json.dumps(elem)
                )

                print("SQS Customer Response: ", response)

    print("\n---End of Execution---\n")

    return 0
