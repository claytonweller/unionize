from modules.worker.get_workers_in_union import get_workers_in_union
from modules.worker.find_matching_union_worker import find_matching_union_worker
from modules.worker.data_class import Worker
from modules.worker.table import workers_table
from modules.lambda_response import format


from json import loads


def handler(event, context):
    print(event)
    body = loads(event['body'])
    union_workers = get_workers_in_union(body['unionName'])
    match = find_matching_union_worker(union_workers, body['encodedPhone'])
    if not match:
        return format('Worker not found in Union', 404)

    if 'encodedPassword' in match.keys():
        return format('Worker already registered', 401)

    worker_item: Worker = {
        **match,
        'encodedPassword': body['password'],
        'authorized': True
    }

    workers_table.put_item(Item=worker_item)
    # Send confirmation text
    # TODO waiting on my pinpoint number being out of 'pending' status
    # sns.publish(
    #     PhoneNumber="+12223334444",
    #     Message=
    # )

    # Return success response
    response = worker_item
    return format(response)
