from json import dumps
import dataclasses


def format(body, status=200, headers={}):
    dict_body = body.__dict__ if dataclasses.is_dataclass(body) else body
    json_body = dumps(dict_body)
    return {
        "isBase64Encoded": True,
        "statusCode": status,
        "headers": headers,
        "body": json_body
    }
