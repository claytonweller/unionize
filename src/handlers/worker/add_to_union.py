from modules.worker.find_matching_union_worker import find_matching_union_worker
from modules.worker.data_class import Worker
from modules.worker.table import WorkerTable
from modules.worker.sms_messaging import send_authorization_link
from modules.worker.generate_pseudonym import generate_pseydonym
from json import loads


def handler(event, context):
    print(event)
    body = loads(event['Records'][0]['body'])
    union_name = body['union_name']
    worker_table = WorkerTable()
    union_workers = worker_table.get_workers_in_union(union_name)
    worker = parse_worker_from_body(body)
    match = find_matching_union_worker(
        union_workers, worker.phone, worker.email)

    if match and match.invite_accepted:
        # TODO This could definitely be more robust
        print('Worker Already added to union')
        return

    print('New Worker')
    worker_table.upsert(worker)
    print(worker)

    send_authorization_link(worker.phone, union_name)

    return

# TODO there is a bunch of duplication with the stuff in invite.py


def parse_worker_from_body(body) -> Worker:
    union_name = body['union_name']
    worker = body['worker'] if 'worker' in body else body
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
