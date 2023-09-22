from json import loads
from modules.worker.find_matching_union_worker import find_matching_union_worker
from modules.worker.table import WorkerTable

# from boto3 import client

# sns = client('sns')


def handler(event, context):

    print(event)
    body = loads(event['Records'][0]['body'])
    print(body['messageBody'])

    worker_table = WorkerTable()
    worker = worker_table.find_worker_by_phone(body['originationNumber'])
    print(worker)
    return
