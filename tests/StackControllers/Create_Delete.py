#!/usr/bin/env python3
import os
import sys
import argparse
import boto3


def print_numbered_list(items):
    for index, item in enumerate(items, start=1):
        print(f"{index}. {item}")


class CloudFormationDependencyError(Exception):
    pass


def lint_template():
    pass


class CFStack:
    pass


class CFStack:
    def __init__(self, session=boto3.Session(), zone=None):
        self.cf_client = session.client('cloudformation') if zone is None else session.client('cloudformation',
                                                                                              region_name=zone,)

    pass

    def get_stack_info(self):

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
    def __init__(self):
        self.stack_names = self.get_stack_info()

    def confirm_delete(self, skip=False):
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

    def get_stack_info(self):
        stack_names = []
        try:
            cf_client = boto3.client("cloudformation")
            response = cf_client.describe_stacks()
            stacks = response["Stacks"]
            for stack in stacks:
                stack_names.append(stack["StackName"])
            return stack_names
        except Exception as e:
            print("Error, exiting")
            return None

    def delete_selections(self, stack_names):
        cf_client = boto3.client('cloudformation')

        for stack in stack_names:
            try:
                # Delete the stack
                cf_client.delete_stack(StackName=stack)
                print(f"Stack {stack} deletion initiated. Status: Started")

                # Wait for the stack to be deleted
                waiter = cf_client.get_waiter('stack_delete_complete')
                waiter.wait(StackName=stack)
                print(f"Stack {stack} deleted successfully. Status: Deleted")
            except boto3.exceptions.botocore.exceptions.BotoCoreError as e:
                # Check if the stack was deleted despite the error
                try:
                    cf_client.describe_stacks(StackName=stack)
                except boto3.exceptions.botocore.exceptions.BotoCoreError:
                    print(f"Stack {stack} was deleted")


class StackCreator(CFStack):
    def __init__(self, directory):
        """
        Initializes the StackCreator.

        Args:
            directory (str): The directory path where the YAML files are located.
        """
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
                    cf_templates[filename] = template_contents

        return cf_templates

    def create_all_stacks(self, directory=None, stack_mapping=None, failed_map={}):
        """
        Creates all CloudFormation stacks from the YAML files in the specified directory,
        waiting for completion and handling rollback if necessary.

        Args:
            directory (str): The directory path where the YAML files are located.
            stack_mapping (dict): A dictionary containing stack names as keys and template contents as values.
        Returns:
            list of stacks that failed
        """
        if directory is None:
            directory = self.directory

        if stack_mapping is None:
            stack_mapping = self.read_cf_templates(directory)
        max = len(stack_mapping) * 3
        i = 0
        if stack_mapping:
            stack_names = list(stack_mapping.keys())

            for stack_name in stack_names:
                if i > max:
                    return
                template_body = stack_mapping[stack_name]

                try:
                    self._create_stack(stack_name, template_body)
                    print(f"Stack '{stack_name}' creation completed.")
                    stack_mapping.remove(stack_mapping)
                    i += 1

                except CloudFormationDependencyError:
                    print(
                        f"Stack '{stack_name}' creation failed due to dependency error. Moving it to the end of the stack list.")
                    tmp = stack_mapping[stack_name]
                    stack_mapping.remove(stack_name)
                    stack_mapping.append(tmp)
                except Exception as e:
                    print(f"Error creating stack '{stack_name}': {str(e)}")
        else:
            print("No templates were provided")

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
        client = boto3.client("cloudformation", region_name="us-east-1")

        try:
            response = client.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Capabilities=["CAPABILITY_NAMED_IAM", "CAPABILITY_IAM", "CAPABILITY_AUTO_EXPAND"],
                OnFailure="DELETE",
            )
            print(f"Stack '{stack_name}' creation initiated.")

            # Wait for stack completion
            waiter = client.get_waiter("stack_create_complete")
            waiter.wait(StackName=stack_name)
            print(f"Stack '{stack_name}' creation completed.")
        except client.exceptions.ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            if error_code == "ValidationError" and "NoIAM" in error_message:
                raise CloudFormationDependencyError("Dependency error occurred while creating the stack.")
            else:
                raise Exception(f"Error creating stack '{stack_name}': {error_message}")
        except Exception as e:
            raise Exception(f"Error creating stack '{stack_name}': {str(e)}")


def main():
    sys.argv[0] = "-da"
    # Create the argument parser
    parser = argparse.ArgumentParser(description="CloudFormation Stack Management")

    # Add the command-line options
    parser.add_argument("-ca", "--create_all", action="store_true", dest="create_all",
                        help="Create all CloudFormation stacks from YAML files in the specified directory")
    parser.add_argument("-da", "--delete_all", action="store_true", dest="delete_all",
                        help="Delete all CloudFormation stacks")

    # Parse the command-line arguments
    args = parser.parse_args(sys.argv)
    CF = CFStack()
    # Check the specified options and call the respective functions
    if args.create_all:
        StackCreator('.').create_all_stacks()

    elif args.delete_all:
        StackDeleter().confirm_delete()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
