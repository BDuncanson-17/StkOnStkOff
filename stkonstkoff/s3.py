import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class S3Bucket:
    """
    Represents an Amazon S3 Bucket.

    Attributes:
        s3 (botocore.client.S3): A low-level, session-aware Amazon S3 client.
        name (str): The name of the bucket.
        creation_date (datetime): The creation date of the bucket.
        tags (list): The tags associated with the bucket.
    """

    def __init__(self, session=None):
        """
        Initialize an S3Bucket instance.

        Args:
            session (boto3.Session, optional): The boto3 Session instance.
                If None, a new session is created.
        """
        if session is None:
            session = boto3.Session()
        self.s3 = session.client('s3')
        self.name = None
        self.creation_date = None
        self.tags = []

    @staticmethod
    def get_s3_buckets(session=None):
        """
        List all S3 buckets.

        Args:
            session (boto3.Session, optional): The boto3 Session instance.
                If None, a new session is created.

        Returns:
            list[str]: A list of S3 bucket names.
        """
        if session is None:
            session = boto3.Session()
        s3_client = session.client('s3')

        try:
            response = s3_client.list_buckets()
        except ClientError as e:
            print(f"Failed to list S3 buckets: {e}")
            return None

        buckets = [bucket['Name'] for bucket in response['Buckets']]

        return buckets

    def create_bucket(self, bucket_name):
        """
        Create a new S3 bucket.

        Args:
            bucket_name (str): The name of the new bucket.

        Returns:
            str: The name of the newly created bucket.
        """
        try:
            self.s3.create_bucket(Bucket=bucket_name)
            self.name = bucket_name
            print(f"Bucket {bucket_name} created successfully.")
        except ClientError as e:
            print(f"Failed to create bucket {bucket_name}: {e}")
            return None

        return bucket_name

    def delete_bucket(self, bucket_name):
        """
        Delete an S3 bucket.

        Args:
            bucket_name (str): The name of the bucket to delete.

        Returns:
            str: The name of the deleted bucket.
        """
        try:
            self.s3.delete_bucket(Bucket=bucket_name)
            print(f"Bucket {bucket_name} deleted successfully.")
        except ClientError as e:
            print(f"Failed to delete bucket {bucket_name}: {e}")
            return None

        return bucket_name

    def __str__(self):
        """
        Return a string representation of the S3 bucket.

        Returns:
            str: The string representation of the S3 bucket.
        """
        return f's3://{self.name}'


class S3Object(S3Bucket):
    """
    Represents an object in an Amazon S3 Bucket.

    Attributes:
        client (botocore.client.S3): A low-level, session-aware Amazon S3 client.
        bucket (str): The name of the bucket.
        creation_date (datetime): The creation date of the bucket.
        key (str): The key of the object.
        version_id (str): The version ID of the object.
        latest (bool): Whether the object is the latest version.
    """

    def __init__(self, bucket=None, creation_date=None, key=None, version_id=None, latest=None):
        """
        Initialize an S3Object instance.

        Args:
            bucket (str, optional): The name of the bucket.
            creation_date (datetime, optional): The creation date of the bucket.
            key (str, optional): The key of the object.
            version_id (str, optional): The version ID of the object.
            latest (bool, optional): Whether the object is the latest version.
        """
        self.session = boto3.Session()
        self._client = boto3.client("s3")
        self._bucket = bucket
        self._creation_date = creation_date
        self._key = key
        self._version_id = version_id
        self._latest = latest

    # Getters
    @property
    def client(self):
        return self._client

    @property
    def bucket(self):
        return self._bucket

    @property
    def creation_date(self):
        return self._creation_date

    @property
    def key(self):
        return self._key

    @property
    def version_id(self):
        return self._version_id

    @property
    def latest(self):
        return self._latest

    # Setters
    @bucket.setter
    def bucket(self, value):
        self._bucket = value

    @creation_date.setter
    def creation_date(self, value):
        self._creation_date = value

    @key.setter
    def key(self, value):
        self._key = value

    @version_id.setter
    def version_id(self, value):
        self._version_id = value

    @latest.setter
    def latest(self, value):
        self._latest = value

    # Other methods here ...

    def __str__(self):
        """
        Return a string representation of the S3 object.

        Returns:
            str: The string representation of the S3 object.
        """
        if self.version_id and self.key and self.bucket:
            return f"s3://{self.bucket}/{self.key}?versionId={self.version_id}"
        elif self.key and self.bucket:
            return f"s3://{self.bucket}/{self.key}"
        else:
            return "<uninitialized S3Object>"

    def delete_object(self):
        """
        Deletes the object represented by this instance from the S3 bucket.

        Returns:
            bool: True if the deletion was successful, else False.
        """
        try:
            self.client.delete_object(Bucket=self.bucket, Key=self.key)
            return True
        except ClientError as e:
            print(f"Failed to delete object {self.key} in bucket {self.bucket}: {e}")
            return False

    def copy_to(self, target_bucket, target_key=None):
        """
        Copies the object represented by this instance to another location in S3.

        Args:
            target_bucket (str): The name of the target bucket.
            target_key (str, optional): The key of the target object. If not specified, the source key is used.

        Returns:
            bool: True if the copy was successful, else False.
        """
        if target_key is None:
            target_key = self.key

        copy_source = {
            'Bucket': self.bucket,
            'Key': self.key
        }

        try:
            self.client.copy(copy_source, target_bucket, target_key)
            return True
        except ClientError as e:
            print(f"Failed to copy object {self.key} to {target_bucket}/{target_key}: {e}")
            return False

    def move_to(self, target_bucket, target_key=None):
        """
        Moves the object represented by this instance to another location in S3.

        Args:
            target_bucket (str): The name of the target bucket.
            target_key (str, optional): The key of the target object. If not specified, the source key is used.

        Returns:
            bool: True if the move was successful, else False.
        """
        if self.copy_to(target_bucket, target_key):
            return self.delete_object()

        return False

import unittest
class TestS3Object(unittest.TestCase):
    def setUp(self):
        """
        Set up a test S3 object. This assumes you have a bucket named 'test-bucket'
        and an object with key 'test-object.txt' in your S3.
        """
        try:
            self.s3_object = S3Object('test-bucket', key='test-object.txt')
        except NoCredentialsError:
            self.fail("No AWS credentials found")

    def test_get_bucket_name(self):
        """
        Test that the bucket name getter method returns the correct name.
        """
        self.assertEqual(self.s3_object.get_bucket_name(), 'test-bucket')

    def test_get_key(self):
        """
        Test that the key getter method returns the correct key.
        """
        self.assertEqual(self.s3_object.get_key(), 'test-object.txt')

    def test_set_bucket_name(self):
        """
        Test that the bucket name setter method correctly changes the bucket name.
        """
        self.s3_object.set_bucket_name('new-test-bucket')
        self.assertEqual(self.s3_object.get_bucket_name(), 'new-test-bucket')

    # Test the remaining methods...

if __name__ == '__main__':
    unittest.main()
