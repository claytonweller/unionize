from modules.lambda_response import format
from modules.worker.table import WorkerTable
from modules.worker.data_class import Worker
from modules.worker.generate_pseudonym import generate_pseydonym
from modules.worker.find_matching_union_worker import find_matching_union_worker

from json import loads
from boto3 import client

sns = client('sns')


def handler(event, context):
    print(event)
    body = loads(event['body'])
    potential_workers = body['potentialWorkers']
    worker_table = WorkerTable()
    union_name = body['unionName']
    union_workers = worker_table.get_workers_in_union(union_name)

    for potential_worker in potential_workers:
        worker = parse_worker(potential_worker, union_name)
        match = find_matching_union_worker(
            union_workers, worker.phone, worker.email)
        if match:
            # TODO This could definitely be more robust
            print('Worker Already exists')
            continue

        worker_table.upsert(worker)
        sns.publish(
            PhoneNumber=worker.phone,
            Message=f'A coworker wants to talk about starting a union at {union_name}. Reply to this message to opt in.'
        )

    return format(body)

# TODO This is currently a lot of duplication from add_to_union.py


def parse_worker(potential, union_name) -> Worker:
    phone = potential['phone']
    email = potential['email']
    worker = Worker(
        union_name,
        phone,
        email,
        False,
        False,
        generate_pseydonym()
    )
    print(f'Worker - {worker}')
    return worker
