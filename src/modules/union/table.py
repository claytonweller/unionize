from boto3 import resource
from boto3.dynamodb.conditions import Key
from modules.union.data_class import Union, UnionMessage
from dataclasses import dataclass
import os


@dataclass
class UnionItem:
    unionName: str
    messages: list[dict]


class UnionTable:
    def __init__(self):
        self.table_name = os.getenv('UnionTableName')
        dynamo = resource('dynamodb')
        self.table = dynamo.Table(self.table_name)

    def get(self, name) -> Union:
        result = self.table.query(
            KeyConditionExpression=Key('unionName').eq(name))
        items = result['Items']
        mapped = map(self.parse_union_item, items)
        return list(mapped)[0]

    def create(self, name: str) -> Union:
        union = Union(name, [])
        item = self.format_union_item(union)
        self.table.put_item(Item=item)
        return union

    def update(self, union: Union) -> Union:
        item = self.format_union_item(union)
        self.table.put_item(Item=item)
        return union

    def format_union_item(self, union: Union) -> dict:
        def convert(union_message) -> dict:
            if isinstance(union_message, UnionMessage):
                return union_message.__dict__
            return union_message

        message_dicts = map(convert, union.messages)
        return UnionItem(
            union.name,
            list(message_dicts)
        ).__dict__

    def parse_union_item(self, item) -> Union:
        return Union(
            item['unionName'],
            item['messages']
        )
