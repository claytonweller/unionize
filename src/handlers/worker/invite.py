from modules.lambda_response import format
from modules.worker.table import WorkerTable
from json import loads


async def handler(event, context):
    print(event)
    body = loads(event['body'])
    potential_workers = body['potentialWokers']
    worker_table = WorkerTable()
    async for worker in potential_workers:

        worker_table.upsert(worker)

    return format(body)
