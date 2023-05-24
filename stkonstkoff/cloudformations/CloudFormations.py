import boto3
import operator
import botocore.exceptions
from stkonstkoff.stkonstkoff import StkOnStkOffUtlities
from stkonstkoff.UserAuthentication import STKONSTKOFFSESSION


CE1 = botocore.exceptions.NoCredentialsError
CE2 = botocore.exceptions.EndpointConnectionError


class CFStacks:
    def __init__(self,authenticated=None):
        """
        Initializes CFStacks object.

        Args:
            UserAuth (object):
        """
        self.cf_client = None
        self.stacks = None
        self.stack_names = None
        self.deletion_order = None
        if STKONSTKOFFSESSION.session is None:
            self.cf_client = STKONSTKOFFSESSION.validate_session()
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
            stack_mapping = stkonstkoff.StkOnStkOffUtlities.create_stack_map()

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


stk = CFStacks()

StkOnStkOffUtlities.print_numbered_list(stk.get_stack_names())