from modules.lambda_response import format
import boto3
from json import loads


dynamo = boto3.resource('dynamodb')
union_table = dynamo.Table('unionize-unions')


def handler(event, context):
    print(event)
    response = {
        "event": event,
    }
    body = loads(event['body'])

    item = {
        'unionName': body['union-name'],
        'someOtherKey': 'key',
    }
    saved_item = union_table.put_item(Item=item)
    print(saved_item)
    return format(response)
