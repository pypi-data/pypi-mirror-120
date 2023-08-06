import polling2

email_suffix = "1"


def create_ou(org_client, org_id, email_name, email_host, ou_name, account_names):
    """Create an OU and actually create the accounts within it"""
    create_organizational_unit_response = org_client.create_organizational_unit(
        ParentId=org_id,
        Name=ou_name,
    )
    created_accounts = [
        create_account(
            org_client,
            email_name,
            email_host,
            account_name,
        )
        for account_name in account_names
    ]
    created_accounts = wait_for_accounts(
        org_client, [created_account[0] for created_account in created_accounts]
    )
    for account_id in [created_account[1] for created_account in created_accounts]:
        _ = org_client.move_account(
            AccountId=account_id,
            SourceParentId=org_id,
            DestinationParentId=create_organizational_unit_response[
                "OrganizationalUnit"
            ]["Id"],
        )
    return {
        created_account[2]: created_account[1] for created_account in created_accounts
    }


def create_account(org_client, email_name, email_host, account_name):
    """Create an actual account with the specified arguments and return the account id with its name"""
    create_account_response = org_client.create_account(
        Email=email_addr(account_name, email_name, email_host),
        AccountName=account_name,
    )
    return (create_account_response["CreateAccountStatus"]["Id"], account_name)

######################################

def email_addr(suffix, base, host):
    """Return a qualified email address we can use as an account admin"""
    return f"{base}+{suffix}{email_suffix}@{host}"


def org_root_id(org_client):
    """Get the root id for the whole organizations"""
    try:
        _ = org_client.describe_organization()
    except:
        _ = org_client.create_organization(FeatureSet="ALL")
    list_roots_response = org_client.list_roots()
    root_id = list_roots_response["Roots"][0]["Id"]
    return root_id


def account_creation_not_in_progress(describe_create_account_status_response):
    """polling predicate"""
    account_state = describe_create_account_status_response["CreateAccountStatus"][
        "State"
    ]
    return account_state != "IN_PROGRESS"


def wait_for_accounts(org_client, request_ids):
    """Wait untils the account creations are complete"""
    for request_id in request_ids:
        polling2.poll(
            lambda: org_client.describe_create_account_status(
                CreateAccountRequestId=request_id
            ),
            check_success=account_creation_not_in_progress,
            step=60,
            timeout=20 * 60,
        )

    return [
        (
            request_id,
            org_client.describe_create_account_status(
                CreateAccountRequestId=request_id
            )["CreateAccountStatus"]["AccountId"],
            org_client.describe_create_account_status(
                CreateAccountRequestId=request_id
            )["CreateAccountStatus"]["AccountName"],
        )
        for request_id in request_ids
    ]


