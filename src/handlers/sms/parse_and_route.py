from json import loads
from modules.worker.find_matching_union_worker import find_matching_union_worker
from modules.worker.table import WorkerTable

# from boto3 import client

# sns = client('sns')


def handler(event, context):

    print(event)
    body = loads(event['Records'][0]['body'])

    message = body['messageBody'].lower()
    print(message)
    worker_table = WorkerTable()
    phone = body['originationNumber']
    worker = worker_table.find_worker_by_phone(phone)
    if not worker:
        print(f'Unrecognized Number - {phone}')
        return
    if worker.authorized:
        print('Authorized')
        # Send to union message topic
        return
    if 'help' in message:
        print('Help')
        # Create a response flow that sends a help message.
        return
    if 'stop' in message:
        print('worker not interested in receiving more texts')
        # Add a flag to the worker to not receive any more SMS
        return

    print('worker accepts invitation')
    # Send to accept invitaion topic

    return
