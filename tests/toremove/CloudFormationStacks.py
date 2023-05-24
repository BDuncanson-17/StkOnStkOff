import boto3

from stkonstkoff.UserAuthentication import *



class CFStacks:
    def __init__(self,):

        self.stacks = self.set_stacks()



    def has_active_stacks(self):
        response = self.cfn_client.list_stacks(
            StackStatusFilter=['CREATE_IN_PROGRESS', 'CREATE_FAILED', 'CREATE_COMPLETE',
                               'ROLLBACK_IN_PROGRESS', 'ROLLBACK_FAILED',
                               'ROLLBACK_COMPLETE', 'DELETE_IN_PROGRESS',
                               'DELETE_FAILED', 'UPDATE_IN_PROGRESS',
                               'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS',
                               'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_IN_PROGRESS',
                               'UPDATE_ROLLBACK_FAILED', 'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS',
                               'UPDATE_ROLLBACK_COMPLETE', 'REVIEW_IN_PROGRESS'])
        stacks = response['StackSummaries']
        return len(stacks) > 0

    def set_stacks(self):
        if not self.has_active_stacks() or not self.cft_access['describe']:
            print("There are either no stacks to set or you do not have permissions to access stack information")
            return {}

        stacks = {}
        response = self.cfn_client.describe_stacks()
        stacks = response["Stacks"]
        return stacks


# Example usage
your_object = YourClassName()
if your_object.has_active_stacks():
    print
    def current_stack_names(self):
        """
        Retrieves the list of current CloudFormation stacks.

        Returns:
            list: List of current CloudFormation stacks.
        """
        if self.stacks is None or len(self.stacks) > 1:
            print("Currently there are not active stacks")
            return
        stack_names = self.get_stack_names()


    def get_cft_permissions(self):
        """
        Retrieves the CloudFormation permissions based on the delete_flag.

        Returns:
            dict: Dictionary containing the CloudFormation permissions.
        """
        permissions = {
            "describe": self.user.check_boto3_permission("cloudformation:DescribeStacks"),
            "delete": self.user.check_boto3_permission("cloudformation:DeleteStack"),
            "create": self.user.check_boto3_permission("cloudformation:CreateStack")
        }
        return permissions

    def get_stack_names(self):
        """
        Retrieves the names of all CloudFormation stacks.

        Returns:
            list: List of stack names.
        """
        if not self.stacks:
            return []

        return [stack["StackName"] for stack in self.stacks]

    def get_stack_status(self, stack_name):
        """
        Retrieves the status of a CloudFormation stack.

        Args:
            stack_name (str): Name of the CloudFormation stack.

        Returns:
            str: Stack status.
        """
        try:
            response = self.cf_client.describe_stacks(StackName=stack_name)
            stack = response["Stacks"][0]
            return stack["StackStatus"]
        except botocore.exceptions.NoCredentialsError:
            print("Error: Failed to retrieve stack status. AWS credentials not found.")
            return None
        except botocore.exceptions.BotoCoreError as e:
            print("Error: Failed to retrieve stack status. ", e)
            return None
        except IndexError:
            print(f"Error: Stack '{stack_name}' not found.")
            return None

