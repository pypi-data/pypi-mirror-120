import time


def setup_stackset_admin_role(iam_client):
    """In the given account, create the stackset admin role (should be the control account)"""
    stackset_admin_trust_policy = """{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudformation.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
"""
    statckset_admin_policy = """{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "sts:AssumeRole"
            ],
            "Resource": [
                "arn:aws:iam::*:role/AWSCloudFormationStackSetExecutionRole"
            ],
            "Effect": "Allow"
        }
    ]
}"""
    _ = iam_client.create_role(
        RoleName="AWSCloudFormationStackSetAdministrationRole",
        AssumeRolePolicyDocument=stackset_admin_trust_policy,
    )
    waiter = iam_client.get_waiter("role_exists")
    waiter.wait(
        RoleName="AWSCloudFormationStackSetAdministrationRole",
        WaiterConfig={"Delay": 15, "MaxAttempts": 123},
    )
    _ = iam_client.put_role_policy(
        RoleName="AWSCloudFormationStackSetAdministrationRole",
        PolicyName="AssumeRole-AWSCloudFormationStackSetExecutionRole",
        PolicyDocument=statckset_admin_policy,
    )


def setup_stackset_execution_role(iam_client, deployment_account_id):
    """In the given account, create the stackset exe role (should be a target dev account)"""

    stackset_execution_trust_policy = f"""{{
  "Version": "2012-10-17",
  "Statement": [
    {{
      "Effect": "Allow",
      "Principal": {{
        "AWS": "arn:aws:iam::{deployment_account_id}:role/AWSCloudFormationStackSetAdministrationRole"
      }},
      "Action": "sts:AssumeRole"
    }}
  ]
}} 
"""
    try:
        _ = iam_client.create_role(
            RoleName="AWSCloudFormationStackSetExecutionRole",
            AssumeRolePolicyDocument=stackset_execution_trust_policy,
        )
    except:
        time.sleep(20)
        _ = iam_client.create_role(
            RoleName="AWSCloudFormationStackSetExecutionRole",
            AssumeRolePolicyDocument=stackset_execution_trust_policy,
        )
    waiter = iam_client.get_waiter("role_exists")
    waiter.wait(
        RoleName="AWSCloudFormationStackSetExecutionRole",
        WaiterConfig={"Delay": 15, "MaxAttempts": 123},
    )
    _ = iam_client.attach_role_policy(
        RoleName="AWSCloudFormationStackSetExecutionRole",
        PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess",
    )
