from modules.lambda_response import format
from boto3 import resource, client
from json import loads


dynamo = resource('dynamodb')
sns = client('sns')

union_table = dynamo.Table('unionize-unions')
topic_arn = 'arn:aws:sns:us-east-1:487170294390:unionize-union-created'


def handler(event, context):
    print(event)
    response = {
        "event": event,
    }
    body = loads(event['body'])

    item = {
        'unionName': body['unionName'],
        'someOtherKey': 'key',
    }
    saved_item = union_table.put_item(Item=item)
    print(saved_item)

    sns.publish(
        TopicArn=topic_arn,
        Message='created',
        Subject=body['unionName']
    )
    return format(response)
