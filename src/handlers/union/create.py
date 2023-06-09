from modules.lambda_response import format
from boto3 import resource, client
from json import loads, dumps


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
