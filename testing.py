request_requirements = ["username", "password", "value", "secret_id", "request_url"]
credentials = [None, None, None, None, None]

credentials_dict = dict(zip(request_requirements, credentials))

print(credentials_dict)