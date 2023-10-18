import json
from modules.worker.table import WorkerTable
import os
from boto3 import client

accept_sms_invite_topic_arn = os.getenv('WorkerAcceptedSMSInviteTopicARN')
sns = client('sns')


def handler(event, context):

    print(event)
    body = json.loads(event['Records'][0]['body'])

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
    if worker.invite_accepted:
        print('already accepted')
        # TODO remind them to authorize
        return
    if 'help' in message:
        print('Help')
        # TODO Create a response flow that sends a help message.
        return
    if 'stop' in message:
        print('worker not interested in receiving more texts')
        # Add a flag to the worker to not receive any more SMS
        return

    print('worker accepts invitation')
    # Send to accept invitaion topic
    sns.publish(
        TopicArn=accept_sms_invite_topic_arn,
        Message=json.dumps(worker),
        Subject=worker.union_name
    )

    return
