### Contributors: Lamonte Harris
### Description: Clients repository file used to grab data from the database based on the criteria we pass
### to the functions

import bcrypt
from app.database.models import ClientModel
from app.database.engine import engine
from app.sessions.auth_session_data import AuthSessionData
from sqlmodel import Session, select


def find_all_accounts():
    """
    Grabs all generated accounts in the database
    :return: ClientModel|None
    """
    with Session(engine) as db:
        query = select(ClientModel)
        results = db.exec(query).all()
        return results


def find_all_student_accounts():
    """
    Grabs all generated student accounts in the db
    :return: ClientModel|None
    """
    with Session(engine) as db:
        query = select(ClientModel).where(ClientModel.account_type == 3)
        results = db.exec(query).all()
        return results


def find_account(email: str):
    """
    Tries to find the account by email passed if one exists
    :param email:
    :return:
    """
    with Session(engine) as db:
        query = select(ClientModel).where(ClientModel.email == email)
        result = db.exec(query).one_or_none()
        return result


def find_account_by_id(aid: int):
    """
    Tries to find an account by client id (client id can be for root, professors or students)

    :param aid:
    :return: ClientModel|None
    """
    with Session(engine) as db:
        query = select(ClientModel).where(ClientModel.id == aid)
        result = db.exec(query).one_or_none()
        return result


def find_by_session(data: AuthSessionData):
    """
    Tries to find account using the authenticated email session data passed

    :param data:
    :return: ClientModel|None
    """
    user = find_account(data.email)
    if user is not None:
        return user
    return None


def create_root_account():
    """
    This creates a client model object for the root account and stores it in the database using
    :return: void
    """
    pw = create_password("abc123")

    create_client_model(ClientModel(email="root", password=pw, firstname="root", lastname="root", account_type=1))


def create_password(pw: str):
    """
    Creates a random password and returns the bcrypt hash that's salted

    :param pw:
    :return: str
    """
    pw_salt = bcrypt.gensalt(rounds=15)
    return bcrypt.hashpw(pw.encode('utf-8'), pw_salt)


def create_client_model(client: ClientModel):
    """
    Functional way to create a client model to be reused which
    automatically stores the end point in the db

    :param client:
    :return: void
    """
    with Session(engine) as db:
        db.add(client)
        db.commit()