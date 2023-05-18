import requests
class OAuthCredentials:
    def __init__(self, oauth_config_path):
        self.load_from_file(oauth_config_path)
        self.credential_reqs = {'username': 0, 'password': 1, 'value': 2, 'secret_id': 3, 'request_url': 4}

    def load_from_file(self, oauth_config_path):
        # Implement the logic to load values from the file
        pass

    def get_username(self):
        return self.get_line_from_file(self.credential_reqs['username'])

    def get_password(self):
        return self.get_line_from_file(self.credential_reqs['password'])

    def get_value(self):
        return self.get_line_from_file(self.credential_reqs['value'])

    def get_secret_id(self):
        return self.get_line_from_file(self.credential_reqs['secret_id'])

    def get_request_url(self):
        return self.get_line_from_file(self.credential_reqs['request_url'])


