import boto3


def target_account_session(sts_client, target_account_id, region="us-east-1"):
    """Return a boto Session in a target account that can do admin type stuff"""
    assume_role_response = sts_client.assume_role(
        RoleArn=f"arn:aws:iam::{target_account_id}:role/OrganizationAccountAccessRole",
        RoleSessionName="AccountProvisioning",
    )
    credentials = assume_role_response["Credentials"]
    return boto3.Session(
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
        region_name=region,
    )
