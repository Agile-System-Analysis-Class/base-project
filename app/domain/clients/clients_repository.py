import bcrypt
from database.models import ClientModel
from database.engine import engine
from sqlmodel import Session, select
from sessions.auth_session_data import AuthSessionData


def create_professor_models(total: int = 3):
    return create_array_models("teacher", "Jane", "Doe", total, 2)


def create_student_models(total: int = 15):
    return create_array_models("student", "John", "Doe", total, 3)


def create_array_models(email: str, name: str, lname: str, total: int, account_type: int):
    models = []
    t = 0
    pw_salt = bcrypt.gensalt(rounds=15)
    pw = bcrypt.hashpw(b"abc123", pw_salt)

    while t <= total:
        ln = "%s #%d" % (lname, t)
        e = "%s%d@my.stlcc.edu" % (email, t)
        models.append(ClientModel(email=e, password=pw, firstname=name, lastname=ln, account_type=account_type))
        t += 1

    return models

def find_account(email: str):
    with Session(engine) as db:
        query = select(ClientModel).where(ClientModel.email == email)
        result = db.exec(query).one_or_none()
        return result

def find_by_session(data: AuthSessionData):
    user = find_account(data.email)
    if user is not None:
        return user
    return None

def create_root_account():
    pw = create_password("abc123")

    create_client_model(ClientModel(email="root", password=pw, firstname="root", lastname="root", account_type=1))


def create_password(pw: str):
    pw_salt = bcrypt.gensalt(rounds=15)
    return bcrypt.hashpw(pw.encode('utf-8'), pw_salt)

def create_client_model(client: ClientModel):
    with Session(engine) as db:
        db.add(client)
        db.commit()