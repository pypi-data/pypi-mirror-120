from continuous_security_account_setup.account_bootstrap import (
    setup_stackset_admin_role,
    setup_stackset_execution_role,
)
from continuous_security_account_setup.sts import target_account_session
from continuous_security_account_setup.organizations import create_ou


def create_management_ou(org_client, sts_client, org_id, email_name, email_host):
    """Creates the OU for management - picks most of the values and uses lower level create_ou to do the necessary"""
    created_accounts = create_ou(
        org_client,
        org_id,
        email_name,
        email_host,
        "Management",
        ["Logging", "Deployment"],
    )

    target_iam_client = target_account_session(
        sts_client, created_accounts["Deployment"]
    ).client("iam")
    setup_stackset_admin_role(target_iam_client)
    for created_account_id in created_accounts.values():
        iam_client = target_account_session(sts_client, created_account_id).client(
            "iam"
        )
        setup_stackset_execution_role(iam_client, created_accounts["Deployment"])
    return created_accounts["Deployment"]


def create_app_dev_ou(org_client, sts_client, org_id, email_name, email_host, deployment_account_id):
    """Creates the OU for app dev - picks most of the values and uses lower level create_ou to do the necessary"""
    created_accounts = create_ou(
        org_client,
        org_id,
        email_name,
        email_host,
        "AppDevelopment",
        ["AppDev1", "AppDev2"],
    )
    for created_account_id in created_accounts.values():
        iam_client = target_account_session(sts_client, created_account_id).client(
            "iam"
        )
        setup_stackset_execution_role(iam_client, deployment_account_id)
