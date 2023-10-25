from modules.lambda_response import format
from modules.worker.table import WorkerTable
from modules.worker.data_class import Worker
from modules.worker.generate_pseudonym import generate_pseydonym
from modules.worker.sms_messaging import send_worker_invite
from json import loads


def handler(event, context):
    print(event)
    body = loads(event['body'])
    potential_workers = body['potential_workers']
    worker_table = WorkerTable()
    union_name = body['union_name']

    for potential_worker in potential_workers:
        worker = parse_worker(potential_worker, union_name)
        match = worker_table.find_matching_union_worker(
            worker.phone, worker.email, union_name)
        if match:
            # TODO This could definitely be more robust
            print('Worker Already exists')
            continue

        worker_table.upsert(worker)
        send_worker_invite(worker.phone, union_name)

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
