from modules.lambda_response import format
from modules.union.table import UnionTable
from modules.event_emitter import EventEmitter
from json import loads

union_table = UnionTable()
event_emitter = EventEmitter()


def handler(event, _context):
    print(event)
    body = loads(event['body'])
    union_name = body['union_name']
    union = union_table.create(union_name)
    print(union)

    event_emitter.union_created(body, union_name)
    return format(union)
