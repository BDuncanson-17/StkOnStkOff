import boto3

import stkonstkoff.UserAuthentication
import stkonstkoff.UserAuthentication as UserAuth

import boto3
import botocore


class CloudFormationStacks:
    """
    Class for managing CloudFormation stacks.
    """

    def __init__(self):
        """
        Initializes CloudFormationStacks object.
        """
        self.user = stkonstkoff.UserAuthentication.UserAccess()
        self.cf_client = self.user.session.client
        self.stacks = self.current_stacks()
        self.cft_perms = self.get_cft_permissions()
    def current_stacks(self):
        """
        Retrieves the list of current CloudFormation stacks.

        Returns:
            list: List of current CloudFormation stacks.
        """
        response = self.user.session.client("cloudformation").describe_stacks()
        stacks = response["Stacks"]
        return stacks

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

bd = CloudFormationStacks()
print(bd.get_stack_names())