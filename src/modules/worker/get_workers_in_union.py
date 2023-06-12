from modules.worker.table import workers_table
from modules.worker.data_class import Worker
from boto3.dynamodb.conditions import Key


def get_workers_in_union(union_name: str) -> list[Worker]:
    union_workers = workers_table.query(
        KeyConditionExpression=Key('unionName').eq(union_name)
    )
    print(f'UNION_WORKERS - {union_workers}')
    return union_workers['Items']
