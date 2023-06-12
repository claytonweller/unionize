from boto3 import resource
from boto3.dynamodb.conditions import Key
from modules.worker.data_class import Worker
from dataclasses import dataclass


@dataclass
class WorkerItem:
    unionName: str
    encodedContactHash: str
    encodedPhone: str
    encodedEmail: str
    inviteAccepted: bool
    authorized: bool
    pseudonym: str
    encodedPassword: str = ''


class WorkerTable:
    def __init__(self):
        self.table_name = 'unionize-workers'
        dynamo = resource('dynamodb')
        self.table = dynamo.Table(self.table_name)

    def get_workers_in_union(self, union_name: str) -> list[Worker]:
        union_workers = self.table.query(
            KeyConditionExpression=Key('unionName').eq(union_name))
        print(f'UNION_WORKERS - {union_workers}')
        items = union_workers['Items']
        mapped = map(self.parse_worker_item, items)
        return list(mapped)

    def upsert(self, worker: Worker):
        worker_item = self.format_worker_item(worker)
        self.table.put_item(Item=worker_item.__dict__)
        return worker

    def format_worker_item(self, worker: Worker) -> WorkerItem:
        # TODO in the future these will not be stored as plain text
        encoded_phone = worker.phone
        encoded_email = worker.email
        encoded_password = worker.password
        contact_hash = encoded_phone + '#' + encoded_email
        worker_item = WorkerItem(
            worker.union_name,
            contact_hash,
            encoded_phone,
            encoded_email,
            worker.authorized,
            worker.invite_accepted,
            worker.pseudonym,
            encoded_password,
        )
        print(f'WORKER_ITEM - {worker_item}')
        return worker_item

    def parse_worker_item(self, item) -> Worker:
        # TODO in the future these will not be stored as plain text
        decoded_phone = item['encodedPhone']
        decoded_email = item['encodedEmail']
        worker = Worker(
            item['unionName'],
            decoded_phone,
            decoded_email,
            item['inviteAccepted'],
            item['authorized'],
            item['pseudonym'],
            item['encodedPassword'],
        )
        return worker
