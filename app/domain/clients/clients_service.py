### Contributors: Lamonte Harris
### Description: Client services function for helping us reuse functions for the client

import bcrypt

from .clients_repository import find_account


def get_authenticated_user(email: str, pw: str):
    """
    Grabs the authenticated user data from the db if the user and pw is correct

    :param email:
    :param pw:
    :return: ClientModel|None
    """
    account = find_account(email)
    if account is None:
        return account

    password = account.password.encode('utf-8')
    if bcrypt.checkpw(bytes(pw, 'utf-8'), password):
        return account
    return None