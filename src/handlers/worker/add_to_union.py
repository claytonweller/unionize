from modules.worker.generate_pseudonym import generate_pseydonym
from modules.worker.get_workers_in_union import get_workers_in_union
from modules.worker.find_matching_union_worker import find_matching_union_worker
from modules.worker.table import workers_table
from modules.worker.data_class import Worker
from json import loads


def handler(event, context):
    print(event)
    body = loads(event['Records'][0]['body'])

    union_workers = get_workers_in_union(body['unionName'])
    worker_item = format_worker_item(body)
    match = find_matching_union_worker(
        union_workers, worker_item['encodedPhone'])

    if match:
        # TODO This could definitely be more robust
        print('Worker Already exists')
        return

    print('New Worker')
    workers_table.put_item(Item=worker_item)
    print(worker_item)
    return

    # TODO waiting on my pinpoint number being out of 'pending' status
    # sns.publish(
    #     PhoneNumber="+12223334444",
    #     Message=
    # )

####


def format_worker_item(body) -> Worker:
    union_name = body['unionName']
    worker = body['worker']
    phone = worker['phone']
    email = worker['email']
    contact_hash = worker['phone'] + '#' + worker['email']
    worker_item: Worker = {
        'unionName': union_name,
        'encodedContactHash': contact_hash,
        'encodedPhone': phone,
        'encodedEmail': email,
        'authorized': False,
        'pseudonym': generate_pseydonym(),
    }
    print(f'WORKER_ITEM - {worker_item}')
    return worker_item
