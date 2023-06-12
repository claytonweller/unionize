from modules.worker.find_matching_union_worker import find_matching_union_worker
from modules.worker.data_class import Worker
from modules.worker.table import WorkerTable
from modules.lambda_response import format
from json import loads


def handler(event, context):
    print(event)
    body = loads(event['body'])
    worker_table = WorkerTable()
    union_workers = worker_table.get_workers_in_union(body['unionName'])
    match = find_matching_union_worker(union_workers, body['phone'])
    if not match:
        return format('Worker not found in Union', 404)

    if match.password != '':
        return format('Worker already registered', 401)

    match_dict = match.__dict__
    updated_worker_dict = {
        **match_dict,
        'password': body['password'],
        'authorized': True
    }
    updated_worker = Worker(**updated_worker_dict)
    print(updated_worker)
    response = worker_table.upsert(updated_worker)
    # Send confirmation text
    # TODO waiting on my pinpoint number being out of 'pending' status
    # sns.publish(
    #     PhoneNumber="+12223334444",
    #     Message=
    # )

    # Return success response
    return format(response)
