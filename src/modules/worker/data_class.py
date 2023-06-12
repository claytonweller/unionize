from dataclasses import dataclass


@dataclass
class WorkerItem:
    unionName: str
    encodedContactHash: str
    encodedPhone: str
    encodedEmail: str
    inviteAccepted: bool
    authorized: bool
    pseudonym: str
    encodedPassword: str = ''


@dataclass
class Worker:
    union_name: str
    phone: str
    email: str
    invite_accepted: bool
    authorized: bool
    pseudonym: str
    password: str = ''
