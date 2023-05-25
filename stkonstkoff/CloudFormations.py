import boto3
import operator
import botocore.exceptions
import time
import Utilities
from StkDatabase import data_path


CE1 = botocore.exceptions.NoCredentialsError
CE2 = botocore.exceptions.EndpointConnectionError



class CFStacks:
    def __init__(self, sess=stkonstkoff):
        """
        Initializes CFStacks object.

        Args:
            UserAuth (object):
        """
        self.cf_client = None
        self.stacks = None
        self.stack_names = None
        self.deletion_order = None
        if _G_SESSION.session is None:
            self.cf_client = _G_SESSION.validate_session()
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




    def create_stacks(self, template_map=None):
        if template_map is None:
            template_map = Utilities.create_stack_map()

        for stack_name, template_filepath in template_map.items():
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


        def all_or_select(self):
            all_stacks = input("Would you like to delete all stacks or a single stack (y/n or q to quit)?\n")
            if all_stacks.lower() == 'q':
                exit()
            return all_stacks.lower() == 'y'

        def delete_stack_by_number(self, num):
            stack_names = self.get_stack_names()
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

        def delete_all_stacks(self):
            stack_names = self.get_stack_names()
            for stack_name in stack_names:
                self.delete_stack(stack_name)

        @staticmethod
        def print_list_with_numbers(lst):
            for i, item in enumerate(lst, 1):
                print(f"{i}. {item}")
