from modules.lambda_response import format
from json import loads


def handler(event, context):
    print(event)
    body = loads(event['body'])
    return format(body)
