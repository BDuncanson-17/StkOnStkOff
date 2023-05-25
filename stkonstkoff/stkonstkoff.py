import argparse
import boto3
import botocore
from Utilities import Utilities
from CloudFormations import CFStacks


class UserAccess:
    """
    Class for managing user permissions for AWS services.
    """

    def __init__(self):
        """
        Initializes UserAccess object with an AWS session and an attempts counter.
        """
        self.session = boto3.Session()  # AWS session
        self.attempts = 0  # Counter for authentication attempts


    def validate_session(self):
        """
        Validates the session and returns True if successful.
        Prompts the user to enter access keys if no credentials are present.
        Returns False if authentication fails after four attempts.
        """
        self.attempts = 1  # Initialize attempts to 1
        # A loop to try authentication 3 times
        while self.attempts < 4:
            self.attempts += 1
            if self.attempts == 1:
                try:
                    self.session = boto3.Session()  # Try to create an AWS session
                    return True
                except botocore.exceptions.NoCredentialsError:  # Catch no credential error
                    pass
            else:
                try:
                    # Prompt user to enter their AWS credentials
                    access_key = input("Enter your AWS access key ID: ")
                    secret_key = input("Enter your AWS secret access key: ")
                    self.session = boto3.Session(
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key,
                    )
                    return True
                except botocore.exceptions.NoCredentialsError:
                    # If it's the fourth attempt and credentials are still wrong, exit
                    if self.attempts == 4:
                        return False
                        exit()

    @staticmethod
    def change_user():
        """
        Authenticates a new user session by creating a new UserAccess instance.
        """
        new_user = UserAccess()  # Create a new UserAccess object
        return new_user.session  # Return the AWS session for the new user


# # Instantiate global variables
# _G_SESSION = UserAccess()  # Global UserAccess object
#
#     # Delete all or selected stacks
#     _cft = CFStacks()
#     if all:
#         print("Deleting all stacks...")
#         _cft.delete_all_stacks()
#     elif lst is not None:
#         for stack in lst:
#             _cft.delete_stack(stack)
#     else:
#         print("No stack specified for deletion.")
#
# def selection_create(all=False, lst=None):
#     # Create all or selected stacks
#     _cft = CFStacks()
#     if all and lst is not None:
#         print("Creating all stacks...")
#         _cft.create_stacks(lst)
#     else:
#         print("Creating stack...")
#         print("Not set up for individual stack creation.")
#
# def selection_list_stack():
#     # List all active stacks
#     _cft = CFStacks()
#     stacks = _cft.get_stack_names()
#     if stacks:
#         Utilities.print_numbered_list(stacks)
#     else:
#         print("There are no active stacks")

def main():
    _cft = CFStacks()
    Utilities.print_numbered_list(_cft.stacks)
    _cft.delete_all_stacks()
    # Define the argument parser
    # parser
# Execute the main function if the script is run as a standalone program
if __name__ == "__main__":
    main()
