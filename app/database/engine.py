from urllib.parse import quote_plus, quote

from dotenv import dotenv_values
from sqlmodel import create_engine, SQLModel, Session
from . import models # don't remove this, it creates the tables autoloading them

db_env = dotenv_values('.mysql.env')
mysql_db = db_env.get("MYSQL_DATABASE")
mysql_host = db_env.get("MYSQL_HOST")
mysql_user = db_env.get("MYSQL_USER")
mysql_pass = db_env.get("MYSQL_ROOT_PASSWORD")
sql_engine = 'mysql://%s:%s@%s/%s' %(mysql_user, quote(mysql_pass), mysql_host, mysql_db)

engine = create_engine(sql_engine, echo=True)