from modules.lambda_response import format


def handler(event, context):
    print(event)
    response = {
        "event": event
    }
    return format(response)
