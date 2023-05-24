import boto3
import operator
import botocore.exceptions
from ..Utilities import Utilities
from ..UserAuthentication import *


CE1 = botocore.exceptions.NoCredentialsError
CE2 = botocore.exceptions.EndpointConnectionError


class CFStacks:
    def __init__(self,session_object):
        """
        Initializes CFStacks object.

        Args:
            UserAuth (object):
        """
        self.cf_client = None
        self.stacks = None
        self.stack_names = None
        self.deletion_order = None
        if session_object.session is None:
            self.cf_client = session_object.validate_session()
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
        """
        try:
            return boto3.client("cloudformation")
        except (CE1, CE2):
            print("Error: Cannot access CloudFormation client")
            return None

    def get_stack_objects(self):
        """
        Retrieves the stack objects from CloudFormation.
        Returns an empty list if cf_client is None.
        """
        if self.cf_client is None:
            return []
        return self.cf_client.describe_stacks()["Stacks"]

    def stack_by_creation_time(self):
        """
        Returns a dictionary mapping stack names to their creation times,
        sorted from the last created stack to the first created stack.
        Returns an empty dictionary if cf_client is None.
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
        Returns an empty list if cf_client is None.
        """
        if self.cf_client is None:
            return []
        return [stack["StackName"] for stack in self.stacks]




class StackCreator:

    def __init__(self):
        self.cf_client = boto3.client('cloudformation')
        self.template_files = []
        self.template_dir = []
        self.template_map = {}

    @staticmethod
    def prompt_prefix_string():
        add_prefix = str(
            input("Would you like to add a prefix string to the stacks in your set like webpdf- (y/n):\n")).lower()
        if add_prefix == 'n' or add_prefix == 'no':
            return ""
        prefix_str = input("Add the string you want all your stacks to start with:\n")
        return prefix_str




    def create_stacks(self, template_map):
        if template_map is None:
            stack_mapping = Utilities.create_stack_map()

        for stack_name, template_filepath in stack_mapping.items():
            try:
                with open(template_filepath, 'r') as template_file:
                    template_body = template_file.read()

                response = self.cf_client.create_stack(
                    StackName=stack_name,
                    TemplateBody=template_body,
                    Capabilities=['CAPABILITY_NAMED_IAM'],  # Add this capability
                    OnFailure='ROLLBACK'  # Set the stack rollback behavior on failure
                )

                stack_id = response['StackId']
                print(f"Stack creation initiated. Stack ID: {stack_id}")

                print(f"Waiting for stack '{stack_name}' to be created...")
                waiter = self.cf_client.get_waiter('stack_create_complete')
                waiter.wait(StackName=stack_name)

                # After waiting, check the status of the stack
                stack_response = self.cf_client.describe_stacks(StackName=stack_name)
                stack_status = stack_response['Stacks'][0]['StackStatus']

                if stack_status == 'CREATE_COMPLETE':
                    print(f"Stack '{stack_name}' created successfully.")
                else:
                    print(f"Stack failed to complete due to event: {stack_status}")
                    break

            except Exception as e:
                print(f"Failed to create stack '{stack_name}': {str(e)}")
                break

class StackDeletor:
    def __init__(self):
        self.user = UserAccess
        self.cf_client = boto3.client('cloudformation')


    def get_all_stack_names(self):
        response = self.cf_client.list_stacks(StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE'])
        stack_names = [stack['StackName'] for stack in response['StackSummaries']]
        return stack_names

    def delete_stack_by_number(self):
        stack_names = self.get_all_stack_names()
        self.print_list_with_numbers(stack_names)
        idx = int(input("Enter the number of the stack you want to delete: "))
        if 1 <= idx <= len(stack_names):
            self.delete_stack(stack_names[idx - 1])
        else:
            print('Invalid stack index.')

    def delete_stack(self, stack_name):
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

    @staticmethod
    def print_list_with_numbers(items):
        for i, item in enumerate(items, start=1):
            print(f"{i}.) {item}")

    def delete_all_stacks(self):
        stack_names = self.get_all_stack_names()
        for stack_name in stack_names:
            self.delete_stack(stack_name)
