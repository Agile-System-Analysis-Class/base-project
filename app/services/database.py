import os
import MySQLdb
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host': 'host.docker.internal',
    'user': 'root',
    'port': 3306,
    'password': 'SChool123@!',
    'database': 'schooldb'
    # todo: reimplement environment loading
    # 'db': os.getenv('MYSQL_DATABASE'),
    # 'passwd': os.getenv('MYSQL_ROOT_PASSWORD')
}


def conn():
    return MySQLdb.connect(**db_config)
