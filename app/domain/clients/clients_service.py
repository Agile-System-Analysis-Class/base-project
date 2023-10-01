import bcrypt

from .clients_repository import find_account


def get_authenticated_user(email: str, pw: str):
    account = find_account(email)
    if account is None:
        return account

    password = account.password.encode('utf-8')
    if bcrypt.checkpw(bytes(pw, 'utf-8'), password):
        return account
    return None