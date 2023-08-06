"""Main entry point to invocation"""
import argparse
import boto3
from continuous_security_account_setup.org_bootstrap import create_org

# for development purposes to bump emails for uniqueness
email_suffix = ""

def define_arg_parser():
    parser = argparse.ArgumentParser(
        description="Create Organizational structure for Continuous Security liveSeries"
    )
    parser.add_argument(
        "profile",
        default="default",
        help="AWS profile in master account with permission to assume Org role",
    )
    parser.add_argument(
        "email_name",
        help="per account this will register email_name+account_name@email_host, fred in fred@protonmail.com",
    )
    parser.add_argument(
        "email_host",
        help="per account this will register email_name+account_name@email_host, e.g. protonmail.com in fred@protonmail.com",
    )
    parser.add_argument(
        "--region", default="us-east-1", help="the region to operate within"
    )

    return parser


def main():
    parser = define_arg_parser()
    args = parser.parse_args()

    aws_profile_name = args.profile
    region = args.region
    email_name = args.email_name
    email_host = args.email_host

    boto_session = boto3.Session(profile_name=aws_profile_name, region_name=region)

    create_org(boto_session, email_name, email_host)
