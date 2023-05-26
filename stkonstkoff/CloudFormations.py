#!/usr/bin/env python3
import os
import time
import argparse
import boto3





class StackDeletor:
    def __init__(self):
        self.stack_names = self.get_stack_info()

    def confirm_delete(self, skip=False):
        if self.stack_names is None or len(self.stack_names) == 0:
            print("No stacks to delete")
            return

        if skip:
            self.delete_selections(self.stack_names)
            return

        self.print_numbered_list(self.stack_names)
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

    @staticmethod
    def print_numbered_list(items):
        for index, item in enumerate(items, start=1):
            print(f"{index}. {item}")


class StackCreator:
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
                    cf_templates[file_name] = template_contents

        return cf_templates

    def create_all_stacks(self, directory=None, stack_mapping=None):
        """
        Creates all CloudFormation stacks from the YAML files in the specified directory,
        waiting for completion and handling rollback if necessary.

        Args:
            directory (str): The directory path where the YAML files are located.
            stack_mapping (dict): A dictionary containing stack names as keys and template contents as values.
        """
        if directory is None:
            directory = self.directory

        if stack_mapping is None:
            stack_mapping = self.read_cf_templates(directory)

        if stack_mapping:
            stack_names = list(stack_mapping.keys())

            for stack_name in stack_names:
                template_body = stack_mapping[stack_name]

                try:
                    self._create_stack(stack_name, template_body)
                    print(f"Stack '{stack_name}' creation completed.")
                except CloudFormationDependencyError:
                    print(f"Stack '{stack_name}' creation failed due to dependency error. Moving it to the end of the stack list.")
                    stack_names.remove(stack_name)
                    stack_names.append(stack_name)
                except Exception as e:
                    print(f"Error creating stack '{stack_name}': {str(e)}")
        else:
            print("No templates were provided")

    def _create_stack(self, stack_name, template_body):
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
        stkcreator_obj = StackCreator('/templates')
        stkcreator_obj.create_all_stacks()

    elif args.delete_all:
        stack_deletor = StackDeletor()
        stack_deletor.confirm_delete()
    else:
        parser.print_help()


if __name__ == "__main__":
#
#
# # Create an instance of the CloudFormationTemplate class
# cf_template = CloudFormationTemplate()
#
# # Set the template version and description
# cf_template.set_template_version("2010-09-09")
# cf_template.set_description("My CloudFormation Template")
#
# # Add resources to the template
# cf_template.add_resource("MyBucket", {
#     "Type": "AWS::S3::Bucket",
#     "Properties": {
#         "BucketName": "my-bucket",
#         "AccessControl": "Private"
#     }
# })
#
# # Get the final CloudFormation template as a dictionary
# template = cf_template.get_template()
#
# # Print the template
# print(template)
#
#
#
#
# class UserPrompts:
#     def __init__(self):
#         pass
#
# class Validate:
#
#     @staticmethod
#     def validate_string(data, valid_strings):
#         return data in valid_strings
#
#     # Validation of user inputs
#     @staticmethod
#     def aws_stack_name(input_str):
#         # AWS stack name should not exceed 128 characters
#         if len(input_str) > 128:
#             return False
#         # AWS stack name should start with an alphabetic character and can contain alphanumeric characters and hyphens
#         match = re.match(r'^[A-Za-z][A-Za-z0-9-]*$', input_str)
#         return bool(match)
#
#
#     def number_between_bounds(input_str, lower_bound, upper_bound):
#         try:
#             num = int(input_str)
#             # Check if the number lies in the specified range
#             return lower_bound <= num <= upper_bound
#         except ValueError:  # Input was not a number
#             return False
#
#     @staticmethod
#     def validate_filename(input_str):
#         _, file_extension = os.path.splitext(input_str)
#         return file_extension.lower() in ['.yaml', '.json']
#
#
#
#     @staticmethod
#     def validate_yes_no(input_str):
#         return input_str.lower() in ['yes', 'no', 'y', 'n']
#
#     @staticmethod
#     def validate_filename(input_str):
#         _, file_extension = os.path.splitext(input_str)
#         return file_extension.lower() in ['.yaml', '.json']
#
#     def ask_yes_no_question(question, on_yes=None, on_no=None):
#         while True:
#             answer = input(question + " (yes/y or no/n): ").lower().strip()
#
#             if answer in ("yes", "y"):
#                 if on_yes is not None:
#                     func, *args = on_yes
#                     func(*args)
#                 break
#             elif answer in ("no", "n"):
#                 print("You selected 'no'.")
#                 if on_no is not None:
#                     func, *args = on_no
#                     func(*args)
#                 break
#             else:
#                 print("Invalid input. Please answer with 'yes/y' or 'no/n'.")
#
# class StackDeletor:
#     def __init__(self):
#         selections = []
#         self.stack_names = self.get_stack_info()
#
#     def confirm_delete(self, skip=False):
#         if self.selections is None or len(self.selections) == 0:
#             print("No stacks to delete")
#         if skip:
#             return self.delete_selections(self.selections)
#         Printing.print_numbered_list(self.selections)
#         UserPrompts.ask_yes_no_question("Are these the stack you want to delete",
#                                         self.delete_stacks(self.selections),
#                                         exit())
#
#
#
#     def get_stack_info(self):
#         stack_names = []
#         try:
#             cf_client = boto3.client("cloudformation")
#             response = cf_client.describe_stacks()
#             stacks = response["Stacks"]
#             for stack in stacks:
#                 stack_names.append(stack["StackName"])
#             self.stacks = stacks
#             return stack_names
#         except Exception as e:
#             print("Error, exiting")
#             return None
#
#
#
#
#     def delete_selections(self, stack_names):
#         cf_client = boto3.client('cloudformation')
#
#         for stack in stack_names:
#             try:
#                 # Delete the stack
#                 cf_client.delete_stack(StackName=stack)
#
#                 # Wait for the stack to be deleted
#                 waiter = cf_client.get_waiter('stack_delete_complete')
#                 waiter.wait(StackName=stack)
#                 print(f"Stack {stack} deleted successfully.")
#             except boto3.exceptions.botocore.exceptions.BotoCoreError as e:
#                 # Check if the stack was deleted despite the error
#                 try:
#                     cf_client.describe_stacks(StackName=stack)
#                 except boto3.exceptions.botocore.exceptions.BotoCoreError:
#                     print(f"Stack {stack['StackName']} was deleted")
#
#
#
# def create_stacks_in_order(stack_files):
#     cf_client = boto3.client('cloudformation')
#
#     for stack_file in stack_files:
#         with open(stack_file['filename'], 'r') as file:
#             template_body = file.read()
#
#         try:
#             # Create the stack
#             cf_client.create_stack(
#                 StackName=stack_file['stack_name'],
#                 TemplateBody=template_body,
#                 Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
#                 # Include these capabilities if your template includes IAM resources
#             )
#
#             # Wait for the stack to be created
#             print(f"Creating stack: {stack_file['stack_name']}...")
#             waiter = cf_client.get_waiter('stack_create_complete')
#             waiter.wait(StackName=stack_file['stack_name'])
#             print(f"Stack {stack_file['stack_name']} created successfully.")
#         except boto3.exceptions.botocore.exceptions.BotoCoreError as e:
#             print(f"Error creating stack {stack_file['stack_name']}: {str(e)}")


# stack_files = [
#     {'stack_name': 'webpdf-vpc', 'filename': 'webpdf-vpc.yaml'},
#     {'stack_name': 'webpdf-security', 'filename': 'webpdf-security.yaml'},
#     {'stack_name': 'webpdf-web', 'filename': 'webpdf-web.yaml'},
# ]
# create_stacks_in_order(stack_files)

def main():
    delstk = StackDeletor()
    delstk.selections = delstk.get_stack_info()
    sele = delstk.selections
    delstk.delete_selections(sele)


main()







# class ZonesStacks:
#     def __init__(self):
#         self.us_regions = [
#             'us-east-1', 'us-east-2',
#             'us-west-1', 'us-west-2'
#         ]
#
#     def get_stacks(self):
#         all_stacks = {}
#         for region in self.us_regions:
#             try:
#                 client = boto3.client('cloudformation', region_name=region)
#                 stacks = client.list_stacks(StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE'])
#                 stack_names = [stack['StackName'] for stack in stacks['StackSummaries']]
#                 all_stacks[region] = stack_names
#             except (BotoCoreError, ClientError) as error:
#                 print(f"Error fetching stacks from region {region}. Error: {error}")
#         return all_stacks
#
#
# try:
#     zone_stacks = ZoneStacks()
#     all_stacks = zone_stacks.get_stacks()
#
#     for region, stacks in all_stacks.items():
#         print(f'Stacks in {region}:')
#         for stack in stacks:
#             print(stack)
# except Exception as error:
#     print(f"Error occurred: {error}")
#
# class AWSCFStacks:
#     def __init__(self, region_name):
#             """
#             Retrieves information about a CloudFormation stack and stores it in a dictionary.
#
#             Args:
#                 cf_client (boto3.client): A CloudFormation client object.
#                 region_name (str): The name of the AWS region.
#                 stack_name (str): The name of the stack.
#
#             Returns:
#                 dict: A dictionary containing the region name, stack name, and stack description.
#             """
#             self.region_name = None
#             self.stack_info = None
#             self.stack_info = None
#
#     def get_stack_info(cf_client, stack_name):
#         """
#         Retrieves information about a CloudFormation stack and stores it in a StackInformation object.
#
#         Args:
#             cf_client (boto3.client): A CloudFormation client object.
#             stack_name (str): The name of the stack.
#
#         Returns:
#             StackInformation: An object containing the stack name, creation time, and description.
#         """
#         try:
#             response = boto3.Session.client('cloudformations',region_name).describe_stacks()
#
#             # Get the necessary information from the first (and usually only) stack in the response
#
#             stack_info = response['Stacks'][0]
#             creation_time = stack_info['CreationTime']
#             stack_name = stack_info['StackName']  # Returns None if the key doesn't exist
#
#             return StackInformation(stack_stack_name, creation_time, description)
#
#         except Exception as e:
#             print(f"Error getting stack info: {e}")
#             return None
#
#     def check_for_stack(self,self.region_name,)
#         boto3.Session().client('cloudfomation', region_name)
#     def set_data(self):
#         self.stacks_describe = self.get_stack_objects()
#         self.stack_names = self.get_stack_names()
#         self.stack_infomation.
#     def set_cf_client(self):
#         """
#         Creates and returns the CloudFormation client object.
#         If an exception occurs, None is returned.
#
#         Returns:
#             cf_client (boto3.client): CloudFormation client object.
#         """
#         try:
#             return boto3.client("cloudformation")
#         except botocore.exceptions.NoCredentialsError:  # Replace with actual exceptions
#             print("Error: Cannot access CloudFormation client")
#             return None
#
#     def get_stack_objects(self, region):
#         """
#         Retrieves the stack objects from CloudFormation.
#
#         Returns:
#             list: List of stack objects. If cf_client is None, returns empty list.
#         """
#         if self.cf_client is None:
#             return []
#         if self.region is None:
#             return boto3.Session().client('cloudformations').describe_stacks()["Stacks"]
#         else:
#             return self.cf_client.describe_stacks()["Stacks"]
#
#     def stack_by_creation_time(self):
#         """
#         Returns a dictionary mapping stack names to their creation times,
#         sorted from the last created stack to the first created stack.
#
#         Returns:
#             dict: Dictionary of stack names and their creation times. If cf_client is None, returns empty dictionary.
#         """
#         if self.cf_client is None:
#             return {}
#
#         stack_creation_times = {}
#         for stack in self.stacks:
#             stack_name = stack["StackName"]
#             creation_time = stack["CreationTime"]
#             stack_creation_times[stack_name] = creation_time
#
#         sorted_stack_creation_times = dict(
#             sorted(stack_creation_times.items(), key=operator.itemgetter(1), reverse=True))
#         return sorted_stack_creation_times
#
#     def get_stack_names(self, region_name):
#         """
#         Returns a list of stack names.
#
#         Returns:
#             list: List of stack names. If cf_client is None, returns empty list.
#         """
#         if region is not None:
#             return [stack["StackName"] for stack in self.stacks]
#         else:
#             return self.set_cf_client(region_name).Describe().stack["StackName"]
#
#     def delete_stack_by_number(self, num=None):
#         """
#         Deletes a stack based on its position in the list of stacks.
#
#         Args:
#             num (int, optional): The position of the stack in the list. If not provided, it will ask for user input.
#         """
#         stack_names = self.get_stack_names()
#         if num is None:
#             num = int(input("Enter the number of the stack you want to delete: "))
#         if 1 <= num <= len(self.stacks):
#             self.delete_stack(stack_names[num - 1])
#         else:
#             print('Invalid stack index.')
#             exit()
#
#     def delete_stack(self, stack_name):
#         """
#         Deletes a stack.
#
#         Args:
#             stack_name (str): The name of the stack to be deleted.
#         """
#         try:
#             response = self.cf_client.describe_stacks(StackName=stack_name)
#             stack_status = response['Stacks'][0]['StackStatus']
#
#             if stack_status == 'DELETE_COMPLETE':
#                 print(f'Stack "{stack_name}" is already deleted.')
#                 return
#
#             self.cf_client.delete_stack(StackName=stack_name)
#             print(f'Deleting stack "{stack_name}"...')
#
#             while True:
#                 response = self.cf_client.describe_stacks(StackName=stack_name)
#                 stack_status = response['Stacks'][0]['StackStatus']
#
#                 if stack_status in ['DELETE_COMPLETE', 'DELETE_FAILED']:
#                     break
#
#                 time.sleep(5)
#
#             print(f'Stack "{stack_name}" deleted successfully.')
#
#         except Exception as e:
#             print(f'Failed to delete stack "{stack_name}":', str(e))
#
#     def delete_all_stacks(self):
#         """
#         Deletes all stacks.
#         """
#         stack_names = self.get_stack_names()
#         for stack_name in stack_names:
#             self.delete_stack(stack_name)
