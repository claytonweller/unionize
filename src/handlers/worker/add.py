from modules.lambda_response import format
from modules.generate_pseudonym import generate_pseydonym
from boto3 import resource
from boto3.dynamodb.conditions import Key
from json import loads


dynamo = resource('dynamodb')
workers_table = dynamo.Table('unionize-workers')


def get_workers_in_union(union_name):
    union_workers = workers_table.query(
        KeyConditionExpression=Key('unionName').eq(union_name)
    )
    print(f'UNION_WORKERS - {union_workers}')
    return union_workers


def get_matching_union_worker(union_workers, potential_worker):
    def check(worker):
        phone_match = potential_worker['encodedPhone'] == worker['encodedPhone']
        email_match = potential_worker['encodedEmail'] == worker['encodedEmail']
        return phone_match or email_match

    matches = filter(check, union_workers)
    match = next(matches, None)
    print(f'MATCH - {match}')
    return match


def format_worker_item(body):
    union_name = body['unionName']
    worker = body['worker']
    phone = worker['phone']
    email = worker['email']
    contact_hash = worker['phone'] + '#' + worker['email']
    worker_item = {
        'unionName': union_name,
        'encodedContactHash': contact_hash,
        'encodedPhone': phone,
        'encodedEmail': email,
        'authorized': False,
        'pseudonym': generate_pseydonym(),
    }
    print(f'WORKER_ITEM - {worker_item}')
    return worker_item


def handler(event, context):
    print(event)
    body = loads(event['Records'][0]['body'])

    union_workers = get_workers_in_union(body['unionName'])['Items']
    item = format_worker_item(body)
    match = get_matching_union_worker(union_workers, item)

    if match:
        # TODO This could definitely be more robust
        print('Worker Already exists')
        return

    print('New Worker')
    workers_table.put_item(Item=item)
    print(item)
    return

    # TODO waiting on my pinpoint number being out of 'pending' status
    # sns.publish(
    #     PhoneNumber="+12223334444",
    #     Message=
    # )
