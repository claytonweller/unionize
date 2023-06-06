def handler(event, context):
    print(event)
    response = {
        "event": event,
    }
    body = loads(event['body'])
    print(body)

    return format(response)
