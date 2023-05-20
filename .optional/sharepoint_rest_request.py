import requests
from azure.identity import ClientSecretCredential

class OAuthCredentials:
    """
    A class used to represent and manage OAuth credentials.

    ...

    Attributes
    ----------
    oauth_creds_filepath : str
        a string representing the path to the credentials file
    credentials : dict
        a dictionary storing the client_id, tenant_id, and client_secret

    Methods
    -------
    client_id():
        Returns the client id retrieved from the credentials file.
    tenant_id():
        Returns the tenant id retrieved from the credentials file.
    client_secret():
        Returns the client secret retrieved from the credentials file.
    """

    def __init__(self, oauth_creds_filepath):
        self.oauth_creds_filepath = oauth_creds_filepath
        self.credentials = {"client_id": None, "tenant_id": None, "client_secret": None}

    @property
    def client_id(self):
        """Opens the credentials file and sets the client_id from the first line"""
        with open(self.oauth_creds_filepath, 'r') as file:
            lines = file.readlines()
            self.credentials["client_id"] = lines[0].strip() if lines else None
            return self.credentials["client_id"]

    @property
    def tenant_id(self):
        """Opens the credentials file and sets the client_id from the first line"""
        with open(self.oauth_creds_filepath, 'r') as file:
            lines = file.readlines()
            self.credentials["tenant_id"] = lines[1].strip() if len(lines) > 1 else None
            return self.credentials["tenant_id"]

    @property
    def client_secret(self):
        """Opens the credentials file and sets the client_secret from the third line"""
        with open(self.oauth_creds_filepath, 'r') as file:
            lines = file.readlines()
            self.credentials["client_secret"] = lines[2].strip() if len(lines) > 2 else None
            return self.credentials["client_secret"]

from azure.identity import ClientSecretCredential
import requests
class SharePointRestRequest:
    """
       A class used to make REST requests to SharePoint.

       ...

       Attributes
       ----------
       oauth_credentials : OAuthCredentials
           an instance of the OAuthCredentials class
       token_credential : ClientSecretCredential
           a ClientSecretCredential object from the azure.identity library
       access_token : str
           the access token obtained from Azure AD

       Methods
       -------
       make_request(url):
           Makes a GET request to the specified URL using the access token for authorization
       """

    def __init__(self, oauth_credentials):

        self.oauth_credentials = oauth_credentials
        self.token_credential = ClientSecretCredential(
            tenant_id=self.oauth_credentials.tenant_id,
            client_id=self.oauth_credentials.client_id,
            client_secret=self.oauth_credentials.client_secret
        )
        self.access_token = self.token_credential.get_token('https://management.azure.com/.default').token

    def make_request(self, url):
        """
        Makes a GET request to the specified URL.

        Parameters
        ----------
            url : str
                the URL to make the GET request to

        Returns
        -------
        dict
            the JSON response from the GET request

        Raises
        ------
        Exception
            if the GET request returns a status code other than 200
        """

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Request failed with status {response.status_code}')

    def upload_file(self, url, filepath):
        """
        Uploads a file to the specified URL.

        Parameters
        ----------
            url : str
                the URL to upload the file to
            filepath : str
                the path of the file to upload

        Returns
        -------
        dict
            the JSON response from the upload request

        Raises
        ------
        Exception
            if the upload request returns a status code other than 200
        """

        # Open the file in binary mode
        with open(filepath, 'rb') as file:
            # Prepare the headers
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            # Use the 'files' parameter in the POST request to upload the file
            response = requests.post(url, headers=headers, files={'file': file})

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'File upload failed with status {response.status_code}')


