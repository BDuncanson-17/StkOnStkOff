import boto3
from boto3.compat import _warn_deprecated_python
__author__ = 'Bryan Duncanson'
__version__ = '1.0'

DEFAULT_SESSION = None



def setup_stkonstkoff_session(**kwargs):
    global DEFAULT_SESSION
    DEFAULT_SESSION = boto3.Session(*kwargs)

def _get_default_session():
    if DEFAULT_SESSION is None:
        setup_stkonstkoff_session()
    _warn_deprecated_python()
    return DEFAULT_SESSION

def client(*args, **kwargs):
    return _get_default_session().client(*args, **kwargs)


def resource(*args, **kwargs):
    return _get_default_session().resource(*args, **kwargs)
