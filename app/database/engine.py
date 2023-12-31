### Contributors: Lamonte Harris
### Description: Database engine file loads the local mysql credentials
### then creates a connection object using the sqlmodel package which we will use
### across the application to run our sql queries.

from urllib.parse import quote

from dotenv import dotenv_values
from sqlmodel import create_engine
from . import models # don't remove this, it creates the tables autoloading them

db_env = dotenv_values('app/.mysql.env')
mysql_db = db_env.get("MYSQL_DATABASE")
mysql_pass = db_env.get("MYSQL_ROOT_PASSWORD")
mysql_host = db_env.get("MYSQLDB_HOST")
mysql_user = db_env.get("MYSQLDB_USER")
sql_engine = 'mysql://%s:%s@%s/%s' %(mysql_user, quote(str(mysql_pass).encode()), mysql_host, mysql_db)

engine = create_engine(sql_engine, echo=True)