#!/usr/bin/env python3
#!/usr/bin/env python3
import os
import sys
import argparse
import boto3
import botocore
from botocore.exceptions import ClientError


def print_numbered_list(items):
    """
    Prints a numbered list of items.

    Args:
        items (list): The list of items to print.
    """
    for index, item in enumerate(items, start=1):
        print(f"{index}. {item}")


class CloudFormationDependencyError(Exception):
    """
    Exception raised for CloudFormation dependency errors.
    """
    pass


def lint_template():
    """
    Lints the CloudFormation template.
    """
    pass


class CFStack:
    """
    Class representing a CloudFormation stack.
    """
    def __init__(self, session=boto3.Session(), zone=None):
        """
        Initializes the CFStack.

        Args:
            session (boto3.Session, optional): The Boto3 session to use. Defaults to a new session.
            zone (str, optional): The AWS region name. Defaults to None for the default region.
        """
        self.cf_client = session.client('cloudformation') if zone is None else session.client('cloudformation',
                                                                                              region_name=zone,)

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


class StackDeleter(CFStack):
    """
    Class for deleting CloudFormation stacks.
    """
    def __init__(self):
        """
        Initializes the StackDeleter.
        """
        super().__init__()
        self.stack_names = self.get_stack_info()

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

        print_numbered_list(self.stack_names)
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
            except ClientError as e:
                # Check if the stack was deleted despite the error
                try:
                    self.cf_client.describe_stacks(StackName=stack)
                except ClientError:
                    print(f"Stack {stack} was deleted")


class StackCreator(CFStack):
    """
    Class for creating CloudFormation stacks.
    """
    def __init__(self, directory):
        """
        Initializes the StackCreator.

        Args:
            directory (str): The directory path where the YAML files are located.
        """
        super().__init__()
        self.directory = directory

    def read_cf_templates(self, directory):
        """
        Reads the contents of CloudFormation template files in a directory and returns a dictionary.

        Args:
            directory (str): The directory path.

        Returns:
            dict: A dictionary where keys are file names and values are template contents.
        """
        cf_templates = {}

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                with open(file_path, "r") as file:
                    template_contents = file.read()
                    file_name = os.path.splitext(filename)[0]
                    cf_templates[file_name] = template_contents

        return cf_templates

    # def create_all_stacks(self, directory=None, stack_mapping=None, cycles=3):
    #     """
    #     Creates all CloudFormation stacks from the YAML files in the specified directory,
    #     waiting for completion and handling rollback if necessary.
    # 
    #     Args:
    #         directory (str, optional): The directory path where the YAML files are located.
    #         stack_mapping (dict, optional): A dictionary containing stack names as keys and template contents as values.
    #         cycles (int, optional): The number of cycles to attempt creating the stacks. Defaults to 3.
    #
    #     Returns:
    #         bool: True if all stacks were created successfully, False otherwise.
    #     """
    #     if directory is None:
    #         directory = self.directory
    #
    #     if stack_mapping is None:
    #         stack_mapping = self.read_cf_templates(directory)
    #
    #     fail_templates = {}
    #
    #     while len(stack_mapping) and cycles:
    #         for stack_name, template_body in stack_mapping.items():
    #             try:
    #                 response = self.cf_client.describe_stacks(StackName=stack_name)
    #                 # Stack exists, skip creating it
    #                 print(f"Stack '{stack_name}' already exists, skipping creation.")
    #                 continue
    #             except botocore.exceptions.ClientError as e:
    #                 if e.response['Error']['Code'] == 'ValidationError':
    #                     # Stack does not exist, create it
    #                     if self.create_stack(stack_name, template_body):
    #                         del stack_mapping[stack_name]
    #                     else:
    #                         fail_templates[stack_name] = template_body
    #                         del stack_mapping[stack_name]
    #                 else:
    #                     raise
    #
    #         cycles -= 1
    #
    #     if len(fail_templates):
    #         return self.create_all_stacks(None, fail_templates, cycles)
    #     else:
    #         return True

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
            response = self.cf_client.create_stack(
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
        except self.cf_client.exceptions.ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            if error_code == "ValidationError" and "NoIAM" in error_message:
                raise CloudFormationDependencyError("Dependency error occurred while creating the stack.")
            else:
                raise Exception(f"Error creating stack '{stack_name}': {error_message}")
        except Exception as e:
            raise Exception(f"Error creating stack '{stack_name}': {str(e)}")


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="CloudFormation Stack Management")

    # Add the command-line options
    parser.add_argument("-ca", "--create_all", action="store_true", dest="create_all",
                        help="Create all CloudFormation stacks from YAML files in the specified directory")
    parser.add_argument("-da", "--delete_all", action="store_true", dest="delete_all",
                        help="Delete all CloudFormation stacks")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Check the specified options and call the respective functions
    if args.create_all:
        StackCreator('.').create_all_stacks()

    elif args.delete_all:
        StackDeleter().confirm_delete()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
