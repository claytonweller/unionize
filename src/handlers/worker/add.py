
def handler(event, context):
    print(event)
    response = {
        "event": event,
    }

    return format(response)
