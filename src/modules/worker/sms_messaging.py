from boto3 import client
from modules.worker.data_class import Worker
from modules.union.data_class import UnionMessage

sns = client('sns')


def publish(phone, message):
    print(f'message:{message}')
    sns.publish(
        PhoneNumber=phone,
        Message=message
    )


def send_authorization_link(phone, union_name):
    # TODO this url will have to be generated to link the front end to the correct stuff
    message = f'You have been added to {union_name}. Finish signing up here - http://claytonweller.com/'
    publish(phone, message)


def send_union_message(worker: Worker, union_message: UnionMessage):
    # TODO I might have to send multiple messages if the text is too long
    message = f'{union_message.worker_pseudonym}: {union_message.text}'
    publish(worker.phone, message)


def send_union_message_confirmation(phone, union_name):
    message = f'Message successfully sent to {union_name}'
    publish(phone, message)
    return message


def send_worker_signup_confirmation(phone):
    message = "Signed up, text to this number to send messages to your coworkers"
    publish(phone, message)


def send_worker_invite(phone, union_name):
    message = f'A coworker wants to talk about starting a union at {union_name}. Reply to this message to opt in.'
    publish(phone, message)
