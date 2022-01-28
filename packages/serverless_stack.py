from constructs import Construct
from aws_cdk import (
    aws_s3 as s3,
    aws_s3_deployment as s3upload,
    aws_s3_notifications,
    aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    aws_lambda_event_sources,
    aws_logs as logs,
    Duration,
    RemovalPolicy,
    Stack,
    CfnOutput,
)


class ServerlessStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        region_name = "eu-west-1"

        # creating bucket
        # removal_policy = DESTROY, we are indicating that when we remove the stack the bucket
        # must also be deleted, but this is only true if the bucket is empty.

        self.bucket = s3.Bucket(
            self,
            "CsS3LambdaDynamodb_",
            bucket_name="cs-s3-lambda-dynamodb-eu-west-1",
            versioned=False,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=RemovalPolicy.DESTROY,
            enforce_ssl=True,
            auto_delete_objects=True,
        )

        # We upload csv-data to s3 here
        self.s3_upload = s3upload.BucketDeployment(
            self,
            "UploadFileToS3",
            sources=[s3upload.Source.asset("./csv_data")],
            destination_bucket=self.bucket,
            destination_key_prefix="s3-to-ddb/",
        )

        # We create SQS: This SQS will receive lambda messages.

        self.queue_fail_sqs = sqs.Queue(
            self,
            "CsSqsFail",
            queue_name="cs-sqs-fail",
            visibility_timeout=Duration.seconds(600),
        )
        self.dead_letter_sqs = sqs.DeadLetterQueue(
            max_receive_count=50, queue=self.queue_fail_sqs
        )
        self.queue_sqs = sqs.Queue(
            self,
            "CsSqsMain",
            queue_name="cs-sqs-main",
            visibility_timeout=Duration.seconds(600),
            dead_letter_queue=self.dead_letter_sqs,
        )

        # We create Trigger lambada: which is triggered when there is a new file in the bucket.

        self.s3_trigger_lambda = _lambda.Function(
            self,
            "CsTriggerLambda",
            function_name="cs-trigger-lambda-on-s3-puts",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="trigger_lambda_on_s3_puts.lambda_handler",
            timeout=Duration.seconds(300),
            memory_size=1024,
            description="Lambda reading bucket and sending to SQS",
            code=_lambda.Code.from_asset("./lambda/trigger_lambda/"),
            log_retention=logs.RetentionDays.ONE_WEEK,
            environment={
                "ENV_SQS_QUEUE": self.queue_sqs.queue_url,
                "ENV_REGION_NAME": region_name,
            },
        )

        # We add permission to read from S3 and the event that will activate

        self.bucket.grant_read(self.s3_trigger_lambda)
        notification = aws_s3_notifications.LambdaDestination(self.s3_trigger_lambda)
        self.bucket.add_event_notification(s3.EventType.OBJECT_CREATED, notification)
        self.queue_sqs.grant_send_messages(self.s3_trigger_lambda)

        #  We create the DynamoDB table.

        self.ddb_table = ddb.Table(
            self,
            "CsDdbCsvDataFromS3",
            table_name="cs-ddb-csv-data-from-s3",
            partition_key=ddb.Attribute(name="uuid", type=ddb.AttributeType.STRING),
            sort_key=ddb.Attribute(name="Country", type=ddb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY,
            encryption=ddb.TableEncryption.AWS_MANAGED,
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
        )

        # We create the lambda2: which is triggered when receiving an SQS and writes to the DynamoDB.

        self.ddb_writer_lambda = _lambda.Function(
            self,
            "CsWriterLambda",
            function_name="cs-ddb-writer-lambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="ddb_writer_lambda.lambda_handler",
            timeout=Duration.seconds(300),
            memory_size=1024,
            description="Lambda reads SQS and writes to DDB",
            code=_lambda.Code.from_asset("./lambda/writer_lambda/"),
            log_retention=logs.RetentionDays.ONE_WEEK,
            environment={
                "ENV_SQS_QUEUE": self.queue_sqs.queue_url,
                "ENV_REGION_NAME": region_name,
            },
        )

        # Permission to write to table
        self.ddb_table.grant_write_data(self.ddb_writer_lambda)
        self.ddb_writer_lambda.add_environment("TABLE_NAME", self.ddb_table.table_name)

        # Permission to read from SQS on table
        self.queue_sqs.grant_consume_messages(self.ddb_writer_lambda)

        # THE event that triggers the lambda
        event_source = aws_lambda_event_sources.SqsEventSource(
            self.queue_sqs, batch_size=1
        )
        self.ddb_writer_lambda.add_event_source(event_source)

        CfnOutput(self, "SqsQueueMain", value=self.queue_sqs.queue_url)
