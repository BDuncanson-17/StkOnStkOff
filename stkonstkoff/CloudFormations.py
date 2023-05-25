import boto3
import botocore.credentials
import operator
import time


class CFStacks:
    def __init__(self):
        """
        Initializes CFStacks object.

        Args:
            sess (object): The session object.
        """

        self.cf_client = None
        self.stacks = None
        self.stack_names = None
        self.deletion_order = None
        if boto3.Session is None:
            self.cf_client = boto3.Sessions.client('cloudformations')
            self.cf_client = self.set_cf_client()
            self.stacks = self.get_stack_objects()
            self.stack_names = self.get_stack_names()
            self.deletion_order = self.stack_by_creation_time()
        else:
            self.cf_client = self.set_cf_client()
            self.stacks = self.get_stack_objects()
            self.stack_names = self.get_stack_names()
            self.deletion_order = self.stack_by_creation_time()

    def set_cf_client(self):
        """
        Creates and returns the CloudFormation client object.
        If an exception occurs, None is returned.

        Returns:
            cf_client (boto3.client): CloudFormation client object.
        """
        try:
            return boto3.client("cloudformation")
        except botocore.exceptions.NoCredentialsError:  # Replace with actual exceptions
            print("Error: Cannot access CloudFormation client")
            return None

    def get_stack_objects(self):
        """
        Retrieves the stack objects from CloudFormation.

        Returns:
            list: List of stack objects. If cf_client is None, returns empty list.
        """
        if self.cf_client is None:
            return []
        return self.cf_client.describe_stacks()["Stacks"]

    def stack_by_creation_time(self):
        """
        Returns a dictionary mapping stack names to their creation times,
        sorted from the last created stack to the first created stack.

        Returns:
            dict: Dictionary of stack names and their creation times. If cf_client is None, returns empty dictionary.
        """
        if self.cf_client is None:
            return {}

        stack_creation_times = {}
        for stack in self.stacks:
            stack_name = stack["StackName"]
            creation_time = stack["CreationTime"]
            stack_creation_times[stack_name] = creation_time

        sorted_stack_creation_times = dict(
            sorted(stack_creation_times.items(), key=operator.itemgetter(1), reverse=True))
        return sorted_stack_creation_times

    def get_stack_names(self):
        """
        Returns a list of stack names.

        Returns:
            list: List of stack names. If cf_client is None, returns empty list.
        """
        if self.cf_client is None:
            return []
        return [stack["StackName"] for stack in self.stacks]

    def delete_stack_by_number(self, num=None):
        """
        Deletes a stack based on its position in the list of stacks.

        Args:
            num (int, optional): The position of the stack in the list. If not provided, it will ask for user input.
        """
        stack_names = self.get_stack_names()
        if num is None:
            num = int(input("Enter the number of the stack you want to delete: "))
        if 1 <= num <= len(self.stacks):
            self.delete_stack(stack_names[num - 1])
        else:
            print('Invalid stack index.')
            exit()

    def delete_stack(self, stack_name):
        """
        Deletes a stack.

        Args:
            stack_name (str): The name of the stack to be deleted.
        """
        try:
            response = self.cf_client.describe_stacks(StackName=stack_name)
            stack_status = response['Stacks'][0]['StackStatus']

            if stack_status == 'DELETE_COMPLETE':
                print(f'Stack "{stack_name}" is already deleted.')
                return

            self.cf_client.delete_stack(StackName=stack_name)
            print(f'Deleting stack "{stack_name}"...')

            while True:
                response = self.cf_client.describe_stacks(StackName=stack_name)
                stack_status = response['Stacks'][0]['StackStatus']

                if stack_status in ['DELETE_COMPLETE', 'DELETE_FAILED']:
                    break

                time.sleep(5)

            print(f'Stack "{stack_name}" deleted successfully.')

        except Exception as e:
            print(f'Failed to delete stack "{stack_name}":', str(e))

    def delete_all_stacks(self):
        """
        Deletes all stacks.
        """
        stack_names = self.get_stack_names()
        for stack_name in stack_names:
            self.delete_stack(stack_name)
