from modules.union.table import UnionTable
from modules.worker.table import WorkerTable
from modules.union.data_class import UnionMessage, Union
from modules.worker.sms_messaging import send_union_message, send_union_message_confirmation
from json import loads

union_table = UnionTable()
worker_table = WorkerTable()


def handler(event, _context):
    print(event)
    new_message = parse_message_from_event(event)
    union_name = new_message.union_name
    # TODO I don't want to pass around the un hashed phone in messages
    # we'll have to make this an encoded phone at some point.
    sender_phone = new_message.worker_contact_hash

    existing_union = union_table.get(union_name)
    if not existing_union:
        print(f'Union "{union_name}" does not exist')
        return

    if check_is_duplicate_message(existing_union.messages, new_message):
        print(f'Duplicate message')
        return

    send_message_to_union_workers(new_message)
    add_message_to_union_message_history(existing_union, new_message)
    send_union_message_confirmation(sender_phone, union_name)

    return


def parse_message_from_event(event) -> UnionMessage:
    # TODO if we have batched messages this will break
    body = loads(event['Records'][0]['body'])
    return UnionMessage(
        body['union_name'],
        body['iso_date'],
        body['text'],
        body['worker_pseudonym'],
        body['worker_contact_hash']
    )


def check_is_duplicate_message(
    existing_union_messages: list[UnionMessage], new_union_message: UnionMessage
) -> bool:
    is_duplicate_message = False
    for existing_message in existing_union_messages:
        # TODO also do a narrow time window so people don't get filtered for simple phrases.
        worker_match = new_union_message.worker_pseudonym == existing_message.worker_pseudonym
        text_match = new_union_message.text == existing_message.text
        if worker_match and text_match:
            is_duplicate_message = True
    return is_duplicate_message


def send_message_to_union_workers(new_message: UnionMessage) -> None:
    union_workers = worker_table.get_workers_in_union(new_message.union_name)
    for worker in union_workers:
        phone_matches = worker.phone == new_message.worker_contact_hash
        if worker.authorized and not phone_matches:
            send_union_message(worker, new_message)


def add_message_to_union_message_history(
    existing_union: Union, new_message: UnionMessage
) -> None:
    messeges = [*existing_union.messages, new_message]
    union = Union(existing_union.name, messeges)
    union_table.update(union)
