from json import dumps


def format(body, status=200):
    body = dumps(body)
    {
        "isBase64Encoded": True,
        "statusCode": status,
        "headers": {},
        "body": body
    }
