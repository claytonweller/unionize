from modules.hello import hello


def handler(event, context):
    print(event)
    message = hello('Mipsy')

    return {
        "status": "success",
        "message": message
    }
