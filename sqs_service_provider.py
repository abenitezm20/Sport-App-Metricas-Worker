import boto3
import os
import json

QUEUE = os.getenv('METRICS_QUEUE')
NOTIFICATION_QUEUE = os.getenv('METRICS_NOTIFICATION_QUEUE')

class SqsClientListener():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SqsClientListener, cls).__new__(cls)
            session = boto3.Session(
                aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION_NAME')
            )

            cls._instance = session.client('sqs')
        return cls._instance

    @staticmethod
    def dequeue():
        client = SqsClientListener()
        response = client.receive_message(
            QueueUrl=QUEUE,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=0
        )
        return response.get('Messages', [])
    
    @staticmethod
    def delete(receipt_handle):
        client = SqsClientListener()
        client.delete_message(
            QueueUrl=QUEUE,
            ReceiptHandle=receipt_handle
        )


class SqsClientNotification():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SqsClientNotification, cls).__new__(cls)
            session = boto3.Session(
                aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION_NAME')
            )

            cls._instance = session.client('sqs')
        return cls._instance

    @staticmethod
    def enqueue(data):
        client = SqsClientNotification()
        encodedData = json.dumps(data)
        response = client.send_message(
            QueueUrl=os.getenv('METRICS_NOTIFICATION_QUEUE'),
            MessageBody=encodedData
        )
        return response