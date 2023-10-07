import os.path

from sqlmodel import SQLModel
from app.database.engine import engine
from app.domain.clients.clients_repository import find_account, create_root_account


def setup_database_data():
    if os.path.isfile(".setup_complete"):
        print("setup complete")
        return

    # create tables if they don't exist
    SQLModel.metadata.create_all(engine)

    # create root account if it doesn't exist
    account = find_account("root")
    if account is None:
        create_root_account()
        print("root created")

    f = open(".setup_complete", "w+")
    f.close()

def is_setup_complete():
    if os.path.isfile(".setup_complete"):
        return True
    return False