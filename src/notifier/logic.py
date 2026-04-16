import os
import psutil


def get_env_variable(key: str) -> str:
    var = os.getenv(key)
    if not var:
        msg = f'{key} environment variable is not set.'
        raise ValueError(msg)
    return var


def get_remote_users() -> list[str]:
    users = [session.host for session in psutil.users() if session.host]
    return users
