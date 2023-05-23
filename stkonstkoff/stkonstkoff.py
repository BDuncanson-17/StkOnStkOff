import boto3

class UserPermissions:
    def __init__(self):
        self.session = boto3.Session()
        if self.check_boto3_permission():
            self.has_cft_access = True
        self.has_cft_access = False

    def check_boto3_permission(service):
        try:
            # Attempt to create a client or resource object
            client = boto3.client(service)
            return True
        except Exception as e:
            # If an exception occurs, it means the session does not have permission to use Boto3
            return False

    def set_aws_credentials(self, aws_access_key_id, aws_secret_access_key, aws_session_token, region):
        new_session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region
        )
        self.session = new_session
        self.check_boto3_permission("cloudformations")


class CloudFormationStacks:
    def __init__(self, authorized_user=UserPermissions()):
        self.stacks = None
        if authorized_user.has_cft_access:
            self.stacks = self.current_stacksget_user
        self.Creator = None
        self.Deleter = None



    def get_user_stacks(self):
        response = self.client.list_stacks(StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE'])
        stacks = response.get('StackSummaries', [])
        return stacks

    def list_stack_attribute(self):
        if self.stacks is None or len(self.stacks) == 0:
            print("Current no stacks are active")
        for stack in self.stacks:
            print(stack['StackName'])


# Print information about the user stacks
