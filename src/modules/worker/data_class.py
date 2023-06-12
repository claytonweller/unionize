from dataclasses import dataclass


@dataclass
class Worker:
    unionName: str
    encodedContactHash: str
    encodedPhone: str
    encodedEmail: str
    encodedPassword: str
    authorized: bool
    pseudonym: str
