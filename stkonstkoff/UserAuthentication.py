import boto3
import botocore


class UserAccess:
    """
    Class for managing user permissions for AWS services.
    """

    def __init__(self):
        """
        Initializes UserPermissions object.
        """
        self.session = None
        self.has_permission = False  # Flag indicating if user has permission
        self.attempts = 0  # Number of attempts made to obtain permission

        while self.attempts < 3 and not self.has_permission:
            try:
                if self.attempts == 0:
                    self.session = boto3.Session()
                else:
                    session = boto3.Session(
                        aws_access_key_id=access_key, aws_secret_access_key=secret_key
                    )
                self.has_permission = True
                break
            except botocore.exceptions.NoCredentialsError:
                access_key = input("Enter your AWS access key ID: ")
                secret_key = input("Enter your AWS secret access key: ")
                self.attempts += 1
                if self.attempts == 3:
                    exit()
        self.attempts = 0
        self.has_permissions = True  # Flag indicating if user has permissions
        self.zones = ["us-east-1"]  # AWS availability zones
    def change_user(self):
        access_key = input("Enter your AWS access key ID: ")
        secret_key = input("Enter your AWS secret access key: ")
        return boto3.Session(aws_access_key_id=access_key,
                             aws_secret_access_key=secret_key
                            )


    def check_boto3_permission(self, service):
        """
        Checks if the user has permission to use the specified Boto3 service.

        Args:
            service (str): Name of the Boto3 service to check permission for.

        Returns:
            bool: True if user has permission, False otherwise.
        """
        try:
            # Attempt to create a client or resource object
            client = self.session.client(service)
            return True
        except Exception as e:
            # If an exception occurs, it means the session does not have permission to use Boto3
            return False
