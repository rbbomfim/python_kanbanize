from extractors.kanbanize_extractor import getall_tasks
from conectors.controlecarga_connectordb import Controle_Carga
from conectors.kanbanize_connectordb import Kanbanize
from datetime import datetime
from conectors.mysql_connectordb import Base, db_connection, session
from decouple import config
from utils.util import log, debug, info

log('main')

count_incluir = 0
count_update = 0
count_delete = 0
dateHour = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

Base.metadata.create_all(db_connection) # Cria tabela

# Insere registro na tabela de controle
controle = Controle_Carga('Kanbanize', dateHour, None, 'Em Andamento')
controle.insert()
session.commit()

debug("Iniciando extração da api")
start_api = datetime.now()


df_api = getall_tasks(config('BOARDIDS'))


debug("Finalizado a extração da api")
debug(datetime.now() - start_api)

df = df_api.reset_index()

debug("Entrando no laço incluir e atualizar")
start_time = datetime.now()

for index, row in df.iterrows():
    item = Kanbanize.checkitem(row['taskid'])
    if item:
        count_update += 1
        item.update(row)
        session.commit()
    else:
        count_incluir += 1
        item = Kanbanize(row)
        item.insert()
        session.commit()
    data_limite = row['insertDateHour']


debug("Saindo do laço incluir e atualizar")
debug(datetime.now() - start_time)


debug("Entrando no laço da exclusao")
start_excluir = datetime.now()

lista_excluir = Kanbanize.checkitem_delete(data_limite)

if lista_excluir:
    for item in lista_excluir:
        count_delete += 1
        print(f"Deletando o registro de id: {item.taskid}")
        item.delete()
    session.commit()


debug("Saindo no laço da exclusao")
debug(datetime.now() - start_excluir)


# Atualiza registro na tabela de controle
dt_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
controle.update(dt_update, 'Finalizado')
session.commit()

session.close()

info(f"Foram inseridos: {count_incluir} registros")
info(f"Foram alterados: {count_update} registros")
info(f"Foram excluidos: {count_delete} registros")