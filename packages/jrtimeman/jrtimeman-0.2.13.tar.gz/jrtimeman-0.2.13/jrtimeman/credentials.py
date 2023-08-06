import os
from typing import List

from google.oauth2.credentials import Credentials

from . import utils
from .errors import MissingEnvVar


def get_credentials_from_dict(creds: dict) -> Credentials:
    """
    Create and return a google.oauth2.credentials.Credentials
    object from environment variables.
    """
    creds = utils.dict_keys_to_lower(creds)
    return Credentials(**creds,
                       token_uri="https://oauth2.googleapis.com/token")


def get_credentials_from_env() -> Credentials:
    """
    Create and return a google.oauth2.credentials.Credentials
    object from environment variables.

    Expected environment variables names are
    TOKEN
    REFRESH_TOKEN
    CLIENT_ID
    CLIENT_SECRET

    Raises
    ------
    MissingEnvVar
      If not all env vars are available for authentication
    """
    vars_needed = ["TOKEN", "REFRESH_TOKEN", "CLIENT_ID", "CLIENT_SECRET"]
    if not has_env_vars(vars_needed):
        missing = missing_env_vars(vars_needed)
        raise MissingEnvVar(missing)

    return Credentials(
        token=os.environ["TOKEN"],
        refresh_token=os.environ["REFRESH_TOKEN"],
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token"
    )


def has_env_vars(vars: List[str]) -> bool:
    """
    Checks for the presence of all env variable names in vars

    Parameters
    ----------
    vars : list of strings
      names of environment variables to check for
    """
    return all([var in os.environ for var in vars])


def missing_env_vars(vars: List[str]) -> List[str]:
    """
    Given names of env vars to look for return a list of those which are
    missing.

    Parameters
    ----------
    vars : list of strings
      names of environment variables to check for
    """
    return [var for var in vars if var not in os.environ]
