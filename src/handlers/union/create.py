def handler(event, context):
    print(event)

    return {
        "status": "success",
        "message": event
    }
