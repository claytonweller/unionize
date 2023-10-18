from modules.lambda_response import format
from boto3 import resource, client
from json import loads, dumps
import os

topic_arn = os.getenv('UnionCreatedTopicARN')
table_name = os.getenv('UnionTableName')

dynamo = resource('dynamodb')
sns = client('sns')
union_table = dynamo.Table(table_name)


def handler(event, context):
    print(event)
    response = {
        "event": event,
    }
    body = loads(event['body'])
    union_name = body['unionName']

    item = {
        'unionName': union_name,
        'someOtherKey': 'key',
    }
    union_table.put_item(Item=item)
    print(item)

    sns.publish(
        TopicArn=topic_arn,
        Message=event['body'],
        Subject=union_name
    )
    return format(response)
