from modules.worker.table import WorkerTable
from modules.worker.data_class import Worker
from modules.worker.sms_messaging import send_authorization_link
from modules.union.data_class import UnionMessage
from datetime import datetime

import json
import os
from boto3 import client

accept_sms_invite_topic_arn = os.getenv('WorkerAcceptedSMSInviteTopicArn')
union_message_received_topic_arn = os.getenv('UnionMessageReceivedTopicArn')
sns = client('sns')


def handler(event, context):

    print(event)
    body = json.loads(event['Records'][0]['body'])

    message_text = body['messageBody'].lower()
    print(message_text)
    worker_table = WorkerTable()
    phone = body['originationNumber']
    worker = worker_table.find_worker_by_phone(phone)
    if not worker:
        print(f'Unrecognized Number - {phone}')
        return
    if worker.authorized:
        print('Authorized')
        emit_to_union_message_received_topic(worker, message_text)
        return
    if worker.invite_accepted:
        print('already accepted')
        send_authorization_link(phone, worker.union_name)
        return
    if 'help' in message_text:
        print('Help')
        # TODO Create a response flow that sends a help message.
        return
    if 'stop' in message_text:
        print('worker not interested in receiving more texts')
        # Add a flag to the worker to not receive any more SMS
        return

    print('worker accepts invitation')
    # Send to accept invitaion topic
    emit_to_accept_invite_topic(worker)
    return


# TODO at some point we might want an sns emiter class.
def emit_to_union_message_received_topic(worker: Worker, message_text):
    union_message = UnionMessage(
        worker.union_name,
        datetime.now().isoformat(),
        message_text,
        worker.pseudonym,
        # TODO I don't want to be passing around un hashed contact info
        worker.phone
    )
    sns.publish(
        TopicArn=union_message_received_topic_arn,
        Message=json.dumps(union_message.__dict__),
        Subject=worker.union_name
    )


def emit_to_accept_invite_topic(worker: Worker):
    sns.publish(
        TopicArn=accept_sms_invite_topic_arn,
        Message=json.dumps(worker.__dict__),
        Subject=worker.union_name
    )
