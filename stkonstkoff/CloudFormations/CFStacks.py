import boto3
import botocore
import os
from botocore.exceptions import ClientError


def lint_template():
    """
    Lints the CloudFormation template.
    """
    pass


class CFStack:
    """
    Class representing a CloudFormation stack.
    """
    def __init__(self, session=boto3.Session(), template_dir='./data'):
        """
        Initializes the CFStack.

        Args:
            session (boto3.Session, optional): The Boto3 session to use. Defaults to a new session.
            zone (str, optional): The AWS region name. Defaults to None for the default region.
        """
        self.cf_client = session.client('cloudformation')
        self.template_dir = template_dir
        self.stacks = self.get_stack_info()
        self.num_stacks = len(self.stacks)

    def get_stack_info(self):
        """
        Retrieves information about existing stacks.

        Returns:
            list: A list of stack names.
        """
        stack_names = []
        try:
            response = self.cf_client.describe_stacks()
            stacks = response["Stacks"]
            for stack in stacks:
                stack_names.append(stack["StackName"])
            return stack_names
        except Exception as e:
            print("Error, exiting")
            return None


    def confirm_delete(self, skip=False):
        """
        Confirms the deletion of CloudFormation stacks.

        Args:
            skip (bool, optional): Whether to skip the confirmation and delete all stacks. Defaults to False.
        """
        if self.stack_names is None or len(self.stack_names) == 0:
            print("No stacks to delete")
            return

        if skip:
            self.delete_selections(self.stack_names)
            return

        Utilities.print_numbered_list(self.stack_names)
        user_input = input("Are these the stacks you want to delete? (y/n): ")
        if user_input.lower() == "y":
            self.delete_selections(self.stack_names)
        else:
            print("Deletion cancelled.")

    def delete_selections(self, stack_names):
        """
        Deletes the specified CloudFormation stacks.

        Args:
            stack_names (list): A list of stack names to delete.
        """
        for stack in stack_names:
            try:
                # Delete the stack
                self.cf_client.delete_stack(StackName=stack)
                print(f"Stack {stack} deletion initiated. Status: Started")

                # Wait for the stack to be deleted
                waiter = self.cf_client.get_waiter('stack_delete_complete')
                waiter.wait(StackName=stack)
                print(f"Stack {stack} deleted successfully. Status: Deleted")
            except botocore.exceptions.ClientError as e:
                # Check if the stack was deleted despite the error
                try:
                    self.cf_client.describe_stacks(StackName=stack)
                except botocore.exceptions.ClientError :
                    print(f"Stack {stack} was deleted")

    @property
    def read_cf_templates(self):
        """
        Reads the contents of CloudFormation template files in a directory and returns a dictionary.

        Args:
            directory (str): The directory path.

        Returns:
            dict: A dictionary where keys are file names and values are template contents.
        """
        cf_templates = {}
        directory = self.template_directory

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)  # Corrected file_path
            if filename.endswith(".yaml") or filename.endswith('.yml'):
                with open(file_path, "r") as file:
                    template_contents = file.read()
                    file_name = os.path.splitext(filename)[0]
                    cf_templates[file_name] = template_contents
        return cf_templates

    def create_all_stacks(self, cycles=3, stack_mapping=None):
        """
        Creates all CloudFormation stacks from the YAML files in the specified directory.

        Args:
            directory (str): The directory path where the YAML files are located.
            cycles (int): The number of cycles to attempt creating the stacks. Defaults to 3.
        """
        if stack_mapping is None:
            stack_mapping = self.read_cf_templates

        fail_templates = {}

        while len(stack_mapping) and cycles:
            # Create a separate list of keys
            stack_names = list(stack_mapping.keys())

            for stack_name in stack_names:
                try:
                    if self.create_stack(stack_name, stack_mapping[stack_name]):
                        del stack_mapping[stack_name]
                    else:
                        fail_templates[stack_name] = stack_mapping[stack_name]
                        del stack_mapping[stack_name]
                except Exception as e:
                    print(f"Error creating stack '{stack_name}': {str(e)}")
                    fail_templates[stack_name] = stack_mapping[stack_name]
                    del stack_mapping[stack_name]

            # If there were failures, move them back into the stack_mapping for the next cycle
            stack_mapping.update(fail_templates)
            fail_templates.clear()

            cycles -= 1

        if len(stack_mapping):
            print("Could not create the following stacks after all cycles:")
            for stack_name in stack_mapping.keys():
                print(f" - {stack_name}")

    def create_stack(self, stack_name, template_body):
        """
        Creates a CloudFormation stack using the provided template body.

        Args:
            stack_name (str): The name of the stack.
            template_body (str): The CloudFormation template body.

        Raises:
            CloudFormationDependencyError: If a dependency error occurs while creating the stack.
            Exception: If an error occurs while creating the stack.
        """
        try:
            response = self.cf_client.create_stack(  # Corrected recursive call
                StackName=stack_name,
                TemplateBody=template_body,
                Capabilities=["CAPABILITY_NAMED_IAM", "CAPABILITY_IAM", "CAPABILITY_AUTO_EXPAND"],
                OnFailure="DELETE",
            )
            print(f"Stack '{stack_name}' creation initiated.")

            # Wait for stack completion
            waiter = self.cf_client.get_waiter("stack_create_complete")
            waiter.wait(StackName=stack_name)
            print(f"Stack '{stack_name}' creation completed.")
            return True
        except Exception as e:
            print(f"Error creating stack '{stack_name}': {str(e)}")  # Fixed Exception raising
            return False


