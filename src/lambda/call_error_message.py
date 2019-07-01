import boto3
import os
import json

DESTINATION_PHONE_NUMBER = os.getenv('DestinationPhoneNumber')
SOURCE_PHONE_NUMBER = os.getenv('SourcePhoneNumber')
INSTANCE_ID = os.getenv('InstanceId')
CONTACT_FLOW_ID = os.getenv('ContactFlowId')

connect = boto3.client('connect')

def lambda_handler(event: dict, context: dict) -> None:
    message = get_message(event)
    call_message(message)


def get_message(event: dict) -> str:
    messages = json.loads(event['Records'][0]['Sns']['Message'])
    aws_account_id = messages['AWSAccountId']

    message = f'Lambda関数でエラーが発生しました。'
    message += f'対象のAWSアカウントIDは {aws_account_id} です。'

    return message


def call_message(message: str) -> None:
    connect.start_outbound_voice_contact(
        DestinationPhoneNumber=DESTINATION_PHONE_NUMBER,
        ContactFlowId=CONTACT_FLOW_ID,
        InstanceId=INSTANCE_ID,
        SourcePhoneNumber=SOURCE_PHONE_NUMBER,
        Attributes={
            'message': message
        }
    )
