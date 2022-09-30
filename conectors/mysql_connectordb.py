from sqlalchemy import (create_engine, MetaData)
#from datetime import datetime
from decouple import config
from sqlalchemy.orm import declarative_base, sessionmaker
from utils.util import log, error, critical, warning, debug

log('mysql_connectordb')

db_connection_mysql = 'mysql+pymysql://'+config('LOGIN_MYSQL')+':'+config('PASSWORD_MYSQL')+'@'+config('HOST')+':'+config('PORT')+'/'+config('DATA_BASE')+''
try:
    db_connection = create_engine(db_connection_mysql)
    metadata_obj = MetaData()
    Session = sessionmaker(db_connection)
    session = Session()
    Base = declarative_base()
except:
    critical("Não foi possivel se conectar ao banco de dados Mysql")