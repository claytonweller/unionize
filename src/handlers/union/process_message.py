from modules.union.table import UnionTable
from modules.worker.table import WorkerTable
from modules.union.data_class import UnionMessage, Union
from modules.worker.sms_messaging import send_union_message, send_union_message_confirmation
from boto3 import client
from json import loads

sns = client('sns')
union_table = UnionTable()
worker_table = WorkerTable()


def handler(event, _context):
    print(event)
    # TODO if we have batched messages this will break
    body = loads(event['Records'][0]['body'])
    union_name = body['union_name']
    # TODO I don't want to pass around the un hashed phone in messages
    # we'll have to make this an encoded phone at some point.
    phone = body['worker_contact_hash']
    union_message = UnionMessage(
        union_name,
        body['iso_date'],
        body['text'],
        body['worker_pseudonym'],
        phone
    )

    existing_union = union_table.get(union_name)
    if not existing_union:
        print(f'Union "{union_name}" does not exist')
        return

    # TODO check if the message is a duplicate

    union_workers = worker_table.get_workers_in_union(union_name)
    for worker in union_workers:
        phone_matches = worker.phone == phone
        if worker.authorized and not phone_matches:
            send_union_message(worker, union_message)

    messeges = [*existing_union.messages, union_message]
    union = Union(union_name, messeges)
    union_table.update(union)

    send_union_message_confirmation(phone, union_name)

    return
