# File modified under the Apache Licence 2.0 spec. Modified by Aero Technologies.
# Altered how profile is set based on local/remote execution
import logging
import os
import urllib.parse
import hashlib
import hmac
from pathlib import Path
from datetime import datetime

from metaflow.metaflow_config import AERO_ID_TOKEN, AERO_IDENTITY_POOL, AERO_PROVIDER


def get_aws_credentials():
    import boto3

    client = boto3.client('cognito-identity', region_name='eu-west-1')

    try:
        identity_response = client.get_id(
            IdentityPoolId=AERO_IDENTITY_POOL,
            Logins={AERO_PROVIDER: AERO_ID_TOKEN})
    except Exception as e:
        raise Exception(
            "Credentials have expired, please run 'aero account login' again")

    identity_id = identity_response['IdentityId']

    resp = client.get_credentials_for_identity(
        IdentityId=identity_id,
        Logins={AERO_PROVIDER: AERO_ID_TOKEN})

    secret_key = resp['Credentials']['SecretKey']
    access_key = resp['Credentials']['AccessKeyId']
    session_token = resp['Credentials']['SessionToken']
    expiry = resp['Credentials']['Expiration']

    return {
        "access_key": access_key,
        "secret_key": secret_key,
        "token": session_token,
        "expiry_time": expiry.isoformat()
    }


def create_client_credentials():
    import boto3
    from botocore.credentials import RefreshableCredentials
    from botocore.session import get_session

    # Catch if running on Batch
    if 'METAFLOW_INPUT_PATHS_0' in os.environ or 'MANAGED_BY_AWS' in os.environ:
        return boto3.session.Session(
            region_name='eu-west-1'
        )

    session_credentials = RefreshableCredentials.create_from_metadata(
        metadata=get_aws_credentials(),
        refresh_using=get_aws_credentials,
        method='sts-assume-role'
    )

    session = get_session()
    session._credentials = session_credentials
    autorefresh_session = boto3.Session(
        botocore_session=session,
        region_name='eu-west-1'
    )

    try:
        sts = autorefresh_session.client('sts')
        sts.get_caller_identity()
    except:
        raise Exception(
            "Credentials have expired, please run 'aero account login' again")

    return autorefresh_session


AWS_SESSION = create_client_credentials()


def _get_base_session_credentials():
    from metaflow.exception import MetaflowException

    try:
        import boto3
        from botocore.exceptions import ClientError
    except (NameError, ImportError):
        raise MetaflowException(
            "Could not import module 'boto3'. Install boto3 first.")

    credentials = AWS_SESSION.get_credentials()
    # Credentials are refreshable, so accessing your access key / secret key
    # separately can lead to a race condition. Use this to get an actual matched
    # set.
    current_credentials = credentials.get_frozen_credentials()

    return {
        "access_key": current_credentials.access_key,
        "secret_key": current_credentials.secret_key,
        "token": current_credentials.token
    }


def get_aws_client(module, with_error=False, params={}):
    from metaflow.exception import MetaflowException

    try:
        import boto3
        from botocore.exceptions import ClientError
    except (NameError, ImportError):
        raise MetaflowException(
            "Could not import module 'boto3'. Install boto3 first.")

    if with_error:
        return AWS_SESSION.client(module, **params), ClientError
    return AWS_SESSION.client(module, **params)


from aws_requests_auth.aws_auth import AWSRequestsAuth
from aws_requests_auth.boto_utils import get_credentials

class AeroAWSRequestsAuth(AWSRequestsAuth):

    def __init__(self, aws_host, aws_region, aws_service, session):

        super(AeroAWSRequestsAuth, self).__init__(None, None, aws_host, aws_region, aws_service)
        self._refreshable_credentials = session.get_credentials()

    def get_aws_request_headers_handler(self, r):
        # provide credentials explicitly during each __call__, to take advantage
        # of botocore's underlying logic to refresh expired credentials
        credentials = get_credentials(self._refreshable_credentials)
        return self.get_aws_request_headers(r, **credentials)

def get_auth_object(
    url: str,
    region: str = 'eu-west-1', 
    service: str = 'execute-api'
):
    split_url = url.split("/")
    endpoint = split_url[2] # Just the domain
    return AeroAWSRequestsAuth(
        endpoint, region, service, AWS_SESSION
    )

def get_signed_url(
        url: str,
        method: str,
        dt: datetime = None,
        region: str = 'eu-west-1', 
        service: str = 'execute-api', 
        protocol: str = 'https://', 
        query_string_params: str = None,
        payload: str = ""
    ):

    credentials = _get_base_session_credentials()
    # eg: "https://api.aeroplatform.co.uk/service-api/flows/DailyScheduleTest2/runs/15/steps/end/tasks"

    split_url = url.split("/")
    endpoint = split_url[2] # Just the domain
    path = "/".join(split_url[3:]) # All the rest


    if not dt:
        dt = datetime.utcnow()
    now = dt.strftime("%Y%m%dT%H%M%SZ")
    today = dt.strftime("%Y%m%d")


    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = today + '/' + region + \
        '/' + service + '/' + 'aws4_request'
    if query_string_params:
        canonical_querystring = query_string_params
        canonical_querystring += '&X-Amz-Algorithm=' + algorithm
    else:
        canonical_querystring = 'X-Amz-Algorithm=' + algorithm

    canonical_querystring += '&X-Amz-Credential=' + \
        urllib.parse.quote_plus(
            credentials['access_key'] + '/' + credential_scope)
    canonical_querystring += '&X-Amz-Date=' + now
    canonical_querystring += '&X-Amz-SignedHeaders=host'
    canonical_querystring += "&X-Amz-Security-Token=" + credentials['token']

    payload_hash = hashlib.sha256(payload.encode('utf-8')). hexdigest()
    canonical_request = method + ' \n ' + '/' + path + ' \n ' + canonical_querystring + \
        ' \n ' + 'host:' + endpoint + ' \n\n host \n ' + payload_hash
    string_to_sign = algorithm + ' \n ' + now + ' \n ' + credential_scope + \
        ' \n ' + \
        hashlib.sha256(canonical_request .encode('utf-8')). hexdigest()

    signing_key = __signing_key(
        credentials['secret_key'], today, region, service)
    signature = hmac.new(signing_key, (string_to_sign).encode(
        "utf-8"), hashlib.sha256). hexdigest()
    canonical_querystring += '&X-Amz-Signature=' + signature

    request_url = protocol + endpoint + \
        '/' + path + '?' + canonical_querystring

    return request_url


def __sign(key, msg):
    return hmac.new(key, msg .encode('utf-8'), hashlib.sha256). digest()


def __signing_key(key, date, region, service):
    date_key = __sign(('AWS4' + key).encode('utf-8'), date)
    region_key = __sign(date_key, region)
    service_key = __sign(region_key, service)
    signing_key = __sign(service_key, 'aws4_request')
    return signing_key
