from dataclasses import dataclass


@dataclass
class UnionMessage:
    union_name: str
    iso_date: str
    text: str
    worker_pseudonym: str
    worker_contact_hash: str


@dataclass
class Union:
    name: str
    messages: list[UnionMessage]
