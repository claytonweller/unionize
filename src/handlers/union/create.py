from modules.lambda_response import format
from modules.union.table import UnionTable
from boto3 import client
from json import loads
import os

sns = client('sns')
topic_arn = os.getenv('UnionCreatedTopicARN')
union_table = UnionTable()


def handler(event, _context):
    print(event)
    body = loads(event['body'])
    union_name = body['union_name']
    union = union_table.create(union_name)
    print(union)

    sns.publish(
        TopicArn=topic_arn,
        Message=event['body'],
        Subject=union_name
    )
    return format(union)
