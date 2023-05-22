import boto3
import csv


class BotoSession:
    """
    Class representing an AWS user session.
    """

    def __init__(self):
        """
        Initializes an AWSUserSession object.
        """
        # Initialize the session variable
        self.session = None

        # Test if the current credentials are valid
        try:
            # Attempt to create a session object
            self.session = boto3.Session()
        except Exception as e:
            pass

    def input_credentials(self):
        """
        Prompts the user to input AWS access key ID and secret access key and creates a session object with the provided credentials.
        """
        # Prompt the user to enter AWS access key ID and secret access key
        access_key_id = input("Enter AWS Access Key ID: ")
        secret_access_key = input("Enter AWS Secret Access Key: ")

        # Create a session object with the provided credentials
        try:
            self.session = boto3.Session(
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key
            )
        except Exception as e:
            self.session = None
