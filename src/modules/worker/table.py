from boto3 import resource


def create_worker_table_connection():
    dynamo = resource('dynamodb')
    return dynamo.Table('unionize-workers')


workers_table = create_worker_table_connection()
