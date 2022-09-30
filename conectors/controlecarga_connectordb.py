from email.policy import default
from lib2to3.pytree import Base
from sqlalchemy import (update, func, Column, String, DateTime)
from datetime import datetime
from decouple import config
from conectors.mysql_connectordb import Base, session, db_connection
from utils.util import log, error, critical, warning, debug

log('controle_carga_connectordb')

class Controle_Carga(Base):
    __tablename__ = 'controle_carga_test'
    Processo = Column(String(20), primary_key = True)
    Data_Inicio_Carga = Column(DateTime, primary_key = True)
    Data_Fim_Carga = Column(DateTime, nullable = True, default=None)
    Status = Column(String(100), nullable = False)

    def __init__(self, Processo, Data_Inicio_Carga, Data_Fim_Carga, Status):
        self.Processo = Processo
        self.Data_Inicio_Carga = Data_Inicio_Carga
        self.Data_Fim_Carga = Data_Fim_Carga
        self.Status = Status

    def insert(self):
        session.add(self)

    def update(self, Data_Fim_Carga, Status):
        self.Data_Fim_Carga = Data_Fim_Carga
        self.Status = Status