import boto3
import os
import re
from botocore.exceptions import BotoCoreError, ClientError



class AppController:

    def __int__(self):
        self.session = self.aws_session()
        self.sub_controllers = ['cloudformation','s3']
        self.settings_data =
        self.current_object

        def aws_session(self, aws_access_key=None, aws_secret_key=None):
            """
            Create an AWS session using the provided access key and secret key.

            Args:
                aws_access_key (str): AWS access key ID (optional).
                aws_secret_key (str): AWS secret access key (optional).

            Returns:
                boto3.Session or None: AWS session object if created successfully, None otherwise.
            """
            if aws_access_key and aws_secret_key:
                if not self.validate_key_secret_size(aws_access_key, aws_secret_key):
                    print("Invalid key or secret size.")
                    return None

                try:
                    session = boto3.Session(
                        aws_access_key_id=aws_access_key,
                        aws_secret_access_key=aws_secret_key
                    )
                    return session
                except Exception as e:
                    print("Failed to create session with provided credentials.")
                    print(f"Error: {e}")
                    return None
            else:
                try:
                    session = boto3.Session()
                    return session
                except Exception as e:
                    print("Failed to create session without credentials.")
                    print(f"Error: {e}")
                    return None

        def aws_get_credentials(self):
            """
            Prompt the user to enter AWS access key and secret key.

            Returns:
                boto3.Session or None: AWS session object if created successfully, None otherwise.
            """
            access_key = input("Enter your AWS Access Key: ")
            secret_key = input("Enter your AWS Secret Key: ")
            return self.aws_session(access_key, secret_key)

        def validate_key_secret_size(self, aws_access_key, aws_secret_key):
            """
            Validate the string size of AWS access key and secret access key.

            Args:
                aws_access_key (str): AWS access key ID.
                aws_secret_key (str): AWS secret access key.

            Returns:
                bool: True if key and secret sizes are valid, False otherwise.
            """
            if len(aws_access_key) == 20 and len(aws_secret_key) == 40:
                return True
            else:
                return False
class Prompts:
    def __init__main(self, stkonstkoff_object=):

        class Validation:
            @staticmethod
            def validate_user_input(message, validation_func, invalid_entry_function):
                """
                Prompts the user for input based on the provided message and validates the input using the provided validation function.

                Args:
                    message (str): The message to display when prompting the user for input.
                    validation_func (function): The validation function that takes user input as an argument and returns a boolean value.

                Returns:
                    str: The validated user input.
                """
                while True:
                    user_input = input(message)
                    if validation_func(user_input):
                        return user_input
                    else:
                        if invalid_entry_function is None:
                            print("Invalid input Exiting application..")
                            exit()
                        else:
                            return False



        def validate_recursive(input_data, validation_func, max_retries=3):
            """
            Validates the input data using the provided validation function.
            If the validation function returns False, the function calls itself recursively up to the specified maximum number of retries.

            Args:
                input_data: The input data to validate.
                validation_func: The validation function to apply to the input data.
                max_retries (int): The maximum number of retries (default: 3).

            Returns:
                bool: True if the validation succeeds, False otherwise.
            """
            if validation_func(input_data):
                return True
            elif max_retries > 0:
                print("Validation failed. Retrying...")
                return validate_recursive(input_data, validation_func, max_retries - 1)
            else:
                return False

        @staticmethod
        def find_in_object(data, compare_object):
            return data in compare_object

        # Validation of user inputs
        @staticmethod
        def aws_stack_name(input_str):
            # AWS stack name should not exceed 128 characters
            if len(input_str) > 128:
                return False
            # AWS stack name should start with an alphabetic character and can contain alphanumeric characters and hyphens
            match = re.match(r'^[A-Za-z][A-Za-z0-9-]*$', input_str)
            return bool(match)

        def number_between_bounds(input_str, lower_bound, upper_bound):
            try:
                num = int(input_str)
                # Check if the number lies in the specified range
                return lower_bound <= num <= upper_bound
            except ValueError:  # Input was not a number
                return False

        @staticmethod
        def validate_filename(input_str):
            _, file_extension = os.path.splitext(input_str)
            return file_extension.lower() in ['.yaml', '.json']

        @staticmethod
        def validate_yes_no(input_str):
            return input_str.lower() in ['yes', 'no', 'y', 'n']

        @staticmethod
        def validate_filename(input_str):
            _, file_extension = os.path.splitext(input_str)
            return file_extension.lower() in ['.yaml', '.json']

        validate_length
        def ask_yes_no_question(question, on_yes=None, on_no=None):
            while True:
                answer = input(question + " (yes/y or no/n): ").lower().strip()

                if answer in ("yes", "y"):
                    if on_yes is not None:
                        func, *args = on_yes
                        func(*args)
                    break
                elif answer in ("no", "n"):
                    print("You selected 'no'.")
                    if on_no is not None:
                        func, *args = on_no
                        func(*args)
                    break
                else:
                    print("Invalid input. Please answer with 'yes/y' or 'no/n'.")


class StackController:
    def __init__(self, string):

        def validate_length(input_str, length):
            """
            Validates if the input string has a certain length.

            Args:
                input_str (str): The input string to validate.
                length (int): The desired length.

            Returns:
                bool: True if the input string has the desired length, False otherwise.
            """
            return len(input_str) == length

        def confirm_delete(self, skip=False):
            if self.selections is None or len(self.selections) == 0:
                print("No stacks to delete")
            if skip:
                return self.delete_selections(self.selections)
            Printing.print_numbered_list(self.selections)
            UserPrompts.ask_yes_no_question("Are these the stack you want to delete",
                                            self.delete_stacks(self.selections),
                                            exit())



    def get_stack_info(self):
        stack_names = []
        try:
            cf_client = boto3.client("cloudformation")
            response = cf_client.describe_stacks()
            stacks = response["Stacks"]
            for stack in stacks:
                stack_names.append(stack["StackName"])
            self.stacks = stacks
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

                # Wait for the stack to be deleted
                waiter = cf_client.get_waiter('stack_delete_complete')
                waiter.wait(StackName=stack)
                print(f"Stack {stack} deleted successfully.")
            except boto3.exceptions.botocore.exceptions.BotoCoreError as e:
                # Check if the stack was deleted despite the error
                try:
                    cf_client.describe_stacks(StackName=stack)
                except boto3.exceptions.botocore.exceptions.BotoCoreError:
                    print(f"Stack {stack['StackName']} was deleted")



def create_stacks_in_order(stack_files):
    cf_client = boto3.client('cloudformation')

    for stack_file in stack_files:
        with open(stack_file['filename'], 'r') as file:
            template_body = file.read()

        try:
            # Create the stack
            cf_client.create_stack(
                StackName=stack_file['stack_name'],
                TemplateBody=template_body,
                Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
                # Include these capabilities if your template includes IAM resources
            )

            # Wait for the stack to be created
            print(f"Creating stack: {stack_file['stack_name']}...")
            waiter = cf_client.get_waiter('stack_create_complete')
            waiter.wait(StackName=stack_file['stack_name'])
            print(f"Stack {stack_file['stack_name']} created successfully.")
        except boto3.exceptions.botocore.exceptions.BotoCoreError as e:
            print(f"Error creating stack {stack_file['stack_name']}: {str(e)}")



# Set up your command-line interface
parser = argparse.ArgumentParser(description='Create or delete AWS CloudFormation stacks.')
subparsers = parser.add_subparsers(dest='command')

# Subparser for the 'create' command
create_parser = subparsers.add_parser('create','-c', help='Create a new AWS CloudFormation stack.')
create_parser.add_argument('-create--all', help='The {name:filepath} of the stacks to create.', default = [
     {'stack_name': 'webpdf-vpc', 'filename': 'webpdf-vpc.yaml'},
     {'stack_name': 'webpdf-security', 'filename': 'webpdf-security.yaml'},
     {'stack_name': 'webpdf-web', 'filename': 'webpdf-web.yaml'},
]
                           )


# Subparser for the 'delete' command
delete_parser = subparsers.add_parser('delete', help='Delete an existing AWS CloudFormation stack.')
delete_parser.add_argument('-delete--all', help='The name of the stack to delete.',)

# Parse the command-line arguments
args = parser.parse_args()

# Perform the appropriate operation
if args.command == '-create-all':

elif args.command == 'delete':
    delete



# import boto3
# from botocore.exceptions import BotoCoreError, NoCredentialsError
# from Database import AWS_Static_Info
#
#
#
# class ApplicationSession:
#     def __init__(self):
#         self.session = None
#         self.attempts = 0
#
#     def start_session(self, access_key=None, secret_key=None):
#         try:
#             self.session = boto3.Session(
#                 aws_access_key_id=access_key,
#                 aws_secret_access_key=secret_key
#             )
#             print("AWS session started successfully!")
#             self.attempts = 0  # reset attempts if session starts successfully
#         except (BotoCoreError, NoCredentialsError):
#             self.attempts += 1  # increase attempts count on failure
#             print("Invalid AWS credentials, please try again.")
#             if self.attempts < 3:
#                 self.prompt_for_credentials()
#             else:
#                 print("You have reached the maximum number of attempts. Exiting the program.")
#                 exit()
#
#         def input_credentials(self):
#             access_key = input("Enter your AWS access key: ")
#             secret_key = input("Enter your AWS secret access key: ")
#             self.start_session(access_key, secret_key)
#
#
# def main():
#
#
#
#
#
# if __name__ == "__main__":
#     main()
