from boto3 import client

sns = client('sns')


def publish(phone, message):
    print (f'message:{message}')
    sns.publish(
        PhoneNumber=phone,
        Message=message
    )


def send_authorization_link(phone, union_name):
    # TODO this url will have to be generated to link the front end to the correct stuff
    message = f'You have been added to {union_name}. Finish signing up here - http://claytonweller.com/'
    publish(phone, message)
