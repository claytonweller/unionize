from json import dumps


def format(body, status=200, headers={}):
    body = dumps(body)
    return {
        "isBase64Encoded": True,
        "statusCode": status,
        "headers": headers,
        "body": body
    }
