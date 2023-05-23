import argparse
import boto3
from botocore.exceptions import ClientError



class AWSUserCredentials:
    def __init__(self, session=None):
        self.session = session if session else boto3.Session()
        self.check_aws_credentials()
        self.cft_access = None


    def check_aws_credentials(self):
        try:
            self.session.client('sts').get_caller_identity()
            self.authorized = True
        except Exception as e:
            print("Failed to check AWS credentials:", str(e))
            self.authorized = False

    def set_aws_credentials(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--aws_access_key_id", help="Your AWS Access Key ID")
        parser.add_argument("--aws_secret_access_key", help="Your AWS Secret Access Key")
        parser.add_argument("--aws_session_token", help="Your AWS Session Token")
        parser.add_argument("--region", help="AWS Region")
        args = parser.parse_args()

        self.session = boto3.Session(
            aws_access_key_id=args.aws_access_key_id,
            aws_secret_access_key=args.aws_secret_access_key,
            aws_session_token=args.aws_session_token,
            region_name=args.region
        )

    def set_service_iam(self, service='cloudformations'):
        iam = self.session.client('iam')
        try:
            # assuming the user's name is available in the caller identity
            username = self.session.client('sts').get_caller_identity().get('Arn').split('/')[-1]
            policies = iam.list_policies_for_user(UserName=username)
            self. = [policy.get('PolicyName') for policy in policies.get('Policies')]
        except ClientError as e:
            print("Failed to retrieve IAM policies:", str(e))

    # def set_stack_operation(self, operation):
    #     self.set_iam_service('cloudformations')
    #     if self._iam_access is None or len(self._iam_access) == 0:
    #         return None
    #     if operation.lower() == "create":
    #         return "can_create"
    #     elif operation.lower() == :
    #         "delete" = StackDeletor(self.session)
    #     else:
    #         print(f"Invalid operation {operation}")