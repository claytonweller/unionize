from modules.worker.table import WorkerTable
from modules.worker.sms_messaging import send_authorization_link
from modules.event_emitter import EventEmitter
import json

event_emitter = EventEmitter()


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
        event_emitter.union_message_received(worker, message_text)
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
    event_emitter.accept_invite(worker)
    return
