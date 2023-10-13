### Contributors: Lamonte Harris
### Description: Database helpers are functions that we use to setup the database, as well as check if
### the application was set up.

import os.path

from sqlmodel import SQLModel
from app.database.engine import engine
from app.dependencies import ROOT_DIR
from app.domain.clients.clients_repository import find_account, create_root_account

### We run this to set up all database tables and create root accounts
def setup_database_data():
    """if setup complete is set, exit function"""
    if is_setup_complete():
        print("setup complete")
        return

    """create tables if they don't exist"""
    SQLModel.metadata.create_all(engine)

    """create root account if it doesn't exist"""
    account = find_account("root")
    if account is None:
        create_root_account()
        print("root created")

    """create setup file so we can't run this more than we need to"""
    f = open(f"{ROOT_DIR}/.setup_complete", "w+")
    f.close()

# helper function to check if setup file was created
def is_setup_complete():
    if os.path.isfile(f"{ROOT_DIR}/.setup_complete"):
        return True
    return False