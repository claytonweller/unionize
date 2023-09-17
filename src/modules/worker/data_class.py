from dataclasses import dataclass


@dataclass
class Worker:
    union_name: str
    phone: str
    email: str
    invite_accepted: bool
    authorized: bool
    pseudonym: str
    password: str = ''
