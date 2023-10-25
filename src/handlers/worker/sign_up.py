from modules.worker.data_class import Worker
from modules.worker.table import WorkerTable
from modules.lambda_response import format
from modules.worker.sms_messaging import send_worker_signup_confirmation
from json import loads


def handler(event, context):
    print(event)
    body = loads(event['body'])
    worker_table = WorkerTable()
    phone = body['phone'] if 'phone' in body else ''
    email = body['email'] if 'email' in body else ''
    union_name = body['union_name']
    match = worker_table.find_matching_union_worker(phone, email, union_name)
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

    send_worker_signup_confirmation(updated_worker.phone)

    # Return success response
    return format(response)
