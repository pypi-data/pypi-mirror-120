from continuous_security_account_setup.ou_bootstrap import (
    create_management_ou,
    create_app_dev_ou,
)
from continuous_security_account_setup.organizations import org_root_id


def create_org(master_account_boto_session, email_name, email_host):
    """Top level call to create the OUs and accounts we need for the exercises"""
    org_client = master_account_boto_session.client("organizations")
    sts_client = master_account_boto_session.client("sts")

    root_id = org_root_id(org_client)

    deployment_account_id = create_management_ou(org_client, sts_client, root_id, email_name, email_host)
    create_app_dev_ou(org_client, sts_client, root_id, email_name, email_host, deployment_account_id)
