import os
import json
from boto3 import client
from datetime import datetime
from modules.worker.data_class import Worker
from modules.union.data_class import UnionMessage


sns = client('sns')
accept_sms_invite_topic_arn = os.getenv('WorkerAcceptedSMSInviteTopicArn')
union_message_received_topic_arn = os.getenv('UnionMessageReceivedTopicArn')
union_created_topic_arn = os.getenv('UnionCreatedTopicARN')


class EventEmitter:

    def emit(self, topicArn, message, subject):
        is_dict = isinstance(message, dict)
        message_dict = message.__dict__ if not is_dict else message
        print(f'Emitting Event to: {topicArn}')
        sns.publish(
            TopicArn=topicArn,
            Message=json.dumps(message_dict),
            Subject=subject
        )

    def accept_invite(self, worker: Worker):
        self.emit(
            accept_sms_invite_topic_arn, worker, worker.union_name
        )

    def union_message_received(self, worker: Worker, message_text: str):
        union_message = UnionMessage(
            worker.union_name,
            datetime.now().isoformat(),
            message_text,
            worker.pseudonym,
            # TODO I don't want to be passing around un hashed contact info
            worker.phone
        )
        self.emit(
            union_message_received_topic_arn, union_message, worker.union_name
        )

    def union_created(self, body, union_name: str):
        self.emit(
            union_created_topic_arn, body, union_name
        )
