from lib2to3.pytree import Base
from sqlalchemy import (update, Column, Integer, String, DateTime)
from datetime import datetime
from decouple import config
from conectors.mysql_connectordb import Base, session, db_connection
import pandas as pd
from utils.util import log, error, critical, warning, debug

log('kanbanize_connectordb')

class Kanbanize(Base):
    __tablename__ = config('TABLE')
    boardId = Column(Integer, primary_key = True)
    taskid = Column(Integer, primary_key = True)
    parentid = Column(Integer, nullable = True)
    title = Column(String(1000), nullable = False)
    type = Column(String(100), nullable = False)
    assignee = Column(String(500), nullable = True)
    priority = Column(String(100), nullable = False)
    subtasks = Column(Integer, nullable = False)
    subtaskscomplete = Column(Integer, nullable = False)
    leadtime = Column(Integer, nullable = False)
    blocked = Column(Integer, nullable = False)
    boardparent = Column(Integer, nullable = False)
    createdat = Column(DateTime, nullable = False)
    last_move_time = Column(DateTime(), nullable = False)
    workflow_id = Column(Integer, nullable = False)
    workflow_name = Column(String(100), nullable = False)
    columnid = Column(String(100), nullable = False)
    columnname = Column(String(100), nullable = False)
    columnpath = Column(String(100), nullable = False)
    laneid = Column(Integer, nullable = False)
    lanename = Column(String(500), nullable = False)
    reporter = Column(String(500), nullable = False)
    logedtime = Column(Integer, nullable = False)
    updatedat = Column(DateTime, nullable = False)
    insertDateHour = Column(DateTime, nullable = False)
 
    def __init__(self, df):
        self.df_api = df
        self.boardId = df.boardId
        self.taskid = df.taskid
        self.parentid = df.parentid
        self.title = df.title
        self.type = df.type
        self.assignee = df.assignee
        self.priority = df.priority
        self.subtasks = df.subtasks
        self.subtaskscomplete = df.subtaskscomplete
        self.leadtime = df.leadtime
        self.blocked = df.blocked
        self.boardparent = df.boardparent
        self.createdat = df.createdat
        self.last_move_time = df.last_move_time
        self.workflow_id = df.workflow_id
        self.workflow_name = df.workflow_name
        self.columnid = df.columnid
        self.columnname = df.columnname
        self.columnpath = df.columnpath
        self.laneid = df.laneid
        self.lanename = df.lanename
        self.reporter = df.reporter
        self.logedtime = df.logedtime
        self.updatedat = df.updatedat
        self.insertDateHour = df.insertDateHour        
    
    @classmethod
    def checkitem(cls, taskid):
        debug("Entrando no laço de checar")
        start_time = datetime.now()

        item = session.query(Kanbanize).filter(Kanbanize.taskid == taskid).first()
        if item:
            debug("Entrando no laço de checar = True")
            debug(datetime.now() - start_time)
            return item
        else:
            debug("Entrando no laço de checar = False")
            debug(datetime.now() - start_time)
            return False
   
    @classmethod
    def checkitem_delete(cls, data_limite):
        itens = session.query(Kanbanize).filter(Kanbanize.insertDateHour != data_limite).all()
        if itens:
            return itens
        else:
            return False

    def insert(self):
        session.add(self)

    def update(self, row):
        dict_row = row.to_dict()
        del dict_row['index']
        for key, value in dict_row.items():
            setattr(self, key, value)

    def delete(self):
        session.delete(self)