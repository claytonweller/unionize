from json import loads
# from boto3 import client

# sns = client('sns')


def handler(event, context):
    print(event)
    body = loads(event['Records'][0]['body'])
    print(body['messageBody'])
