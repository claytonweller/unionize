from modules.worker.find_matching_union_worker import find_matching_union_worker
from modules.worker.data_class import Worker
from modules.worker.table import WorkerTable
from modules.worker.generate_pseudonym import generate_pseydonym
from json import loads
from boto3 import client

sns = client('sns')


def handler(event, context):
    print(event)
    body = loads(event['Records'][0]['body'])
    union_name = body['unionName']
    worker_table = WorkerTable()
    union_workers = worker_table.get_workers_in_union(union_name)
    worker = parse_worker_from_body(body)
    match = find_matching_union_worker(
        union_workers, worker.phone, worker.email)

    if match:
        # TODO This could definitely be more robust
        print('Worker Already exists')
        return

    print('New Worker')
    worker_table.upsert(worker)
    print(worker)

    sns.publish(
        PhoneNumber=worker.phone,
        Message=f'You have been added to {union_name}. Finish signing up here - http----.'
    )

    return

# TODO there is a bunch of duplication with the stuff in invite.py


def parse_worker_from_body(body) -> Worker:
    union_name = body['unionName']
    worker = body['worker']
    phone = worker['phone']
    email = worker['email']
    worker = Worker(
        union_name,
        phone,
        email,
        True,
        False,
        generate_pseydonym()
    )
    print(f'Worker - {worker}')
    return worker
