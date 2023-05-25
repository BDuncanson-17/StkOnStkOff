import boto3
import botocore


class UserAccess:
    """
    Class for managing user permissions for AWS services.
    """

    def __init__(self):
        """
        Initializes UserAccess object.
        """
        self.session = boto3.Session()
        self.attempts = 0


    def validate_session(self):
        """
        Validates the session and returns True if successful.
        Prompts the user to enter access keys if no credentials are present.
        Returns False if authentication fails after four attempts.
        """
        self.attempts = 1
        self.session
        while self.attempts < 4:
            self.attempts += 1
            if self.attempts == 1:
                try:
                    self.session = boto3.Session()
                    return True
                except botocore.exceptions.NoCredentialsError:
                    pass
            else:
                try:
                    access_key = input("Enter your AWS access key ID: ")
                    secret_key = input("Enter your AWS secret access key: ")
                    self.session = boto3.Session(
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key,
                    )
                    return True
                except botocore.exceptions.NoCredentialsError:
                    if self.attempts == 4:
                        return False
                        exit()

    @staticmethod
    def change_user():
        """
        Authenticates a new user session by creating a new UserAccess instance.
        """
        new_user = UserAccess()
        return new_user.session

