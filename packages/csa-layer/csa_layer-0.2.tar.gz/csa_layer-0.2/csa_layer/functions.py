import boto3
from botocore.exceptions import ClientError

from .constants import REGION_NAME

def get_secret(secretId, regionName=REGION_NAME):

    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=regionName
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secretId
        )
    except ClientError as e:
        raise e
    secret = get_secret_value_response['SecretString']

    return secret

def add_offender(offId, identifier, reason, region=None):
    offender = {'_id': offId,
                'region': region,
                'identifier': identifier,
                'reason':  reason
            }

    return offender
        