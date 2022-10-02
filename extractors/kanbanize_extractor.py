import sys, os
import requests
import json
import pandas as pd
import xmltodict
from datetime import datetime
from decouple import config
from utils.util import log, error, critical, warning, debug, info


log('kanbanize_extrator')

def login():
    url = config('KANBANIZE_URL') + "/index.php/api/kanbanize/login/"
    payload = json.dumps({
    "email": config('EMAIL'),
    "pass": config('SENHA')
    })
    headers = {
    'apikey': config('APIKEY'),
    'Content-Type': 'application/xml',
    'Cookie': 'ci_csrf_token=4f0659650f87d7ff4c1eaba1a654af8d'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        login = xmltodict.parse(response.text) # Armazena o response em um objeto e convert em json
        apikey = login['xml']['apikey']
        
        return apikey
    except:
        critical("Falha ao realizar login na API do Kanbanize. Verificar email e senha!")
        sys.exit(1) 

def getProjectsBoards():
    itens=[]
    url = config('KANBANIZE_URL') + "/index.php/api/kanbanize/get_projects_and_boards/"
    payload={}
    headers = {
        'apikey': login(),
        'Cookie': 'ci_csrf_token=4f0659650f87d7ff4c1eaba1a654af8d'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except:
        critical("Falha ao obter os projetos e boards do Kanbanize")
        sys.exit(1)

    response_json = response.text # Armazena o response em um objeto
    xml = xmltodict.parse(response_json) # convert xml para json
    project = xml['xml']['projects']['item']

    debug(project)
 
    if isinstance(project, list):
        for item in project:
            project_id = item['id']
            project_name = item['name']
            project_item = item['boards']['item']
            if isinstance(project_item, list):
                for i in project_item:
                    item_id = i['id']
                    item_name = i['name']
                    itens.append(
                        [
                            project_id,
                            project_name,
                            item_id,
                            item_name
                        ]
                    )
            else:
                item_id = project_item['id']
                item_name = project_item['name']        
                itens.append(
                    [
                        project_id,
                        project_name,
                        item_id,
                        item_name
                    ]
                )
    else:
        project_id = xml['xml']['projects']['item']['id']
        project_name = xml['xml']['projects']['item']['name']
        item_id = xml['xml']['projects']['item']['boards']['item']['id']
        item_name = xml['xml']['projects']['item']['boards']['item']['name']
        itens.append(
            [
                project_id,
                project_name,
                item_id,
                item_name
            ]
        )
    df_project = pd.DataFrame(
            itens,
            columns=[
                'project_id',
                'project_name',
                'item_id',
                'item_name'    
                ]
    )

    return df_project

def getall_tasks(boardids): 
    info("Iniciando o processo de leitura da API de GetAllTasks")
    if boardids:
        itensId = [int(x) for x in boardids.split(',')]
        df_itemId = pd.DataFrame(itensId, columns=['item_id'])
        itemId = df_itemId['item_id']
        info("Processo de leitura de GetAllTasks baseado nos Ids informados")
    else:
        info("Processo de leitura de GetAllTasks baseado no nível de acesso do usuário")
        df_project = getProjectsBoards()
        itemId = df_project.item_id

    dateHour = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fields=[]
    
    url = config('KANBANIZE_URL') + "/index.php/api/kanbanize/get_all_tasks/"
    df = itemId.reset_index()

    for index, row in df.iterrows():
        itemId = row['item_id']
        payload = json.dumps({
        "boardid": int(itemId),
        "column": "",
        "comments": "yes",
        "textformat": "",
        "lane": "",
        "section": ""
        })
        headers = {
        'apikey': login(),
        'Content-Type': 'application/xml',
        'Cookie': 'ci_csrf_token=4f0659650f87d7ff4c1eaba1a654af8d'
        }
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
        except:
            error("Falha ao obter as tasks do projeto/item: " + str(itemId))

        data = response.text # Armazena o response em um objeto
        xml = xmltodict.parse(data) # convert xml para json
        
        try:
            root = xml['xml']['item']

            debug(xml)

            for field in root: # Percorre o laço do <xml><item>
                itemId = itemId
                taskid = field['taskid']
                title = field['title']
                type = field['type']
                assignee = field['assignee']            
                priority = field['priority']
                subtasks = field['subtasks']
                subtaskscomplete = field['subtaskscomplete']
                leadtime = field['leadtime']
                blocked = field['blocked']
                boardparent = field['boardparent']
                createdat = field['createdat']
                last_move_time = field['last_move_time']
                workflow_id = field['workflow_id']
                workflow_name = field['workflow_name']
                columnid = field['columnid']
                columnname = field['columnname']
                columnpath = field['columnpath']
                laneid = field['laneid']
                lanename = field['lanename']
                reporter = field['reporter']
                logedtime = field['logedtime']
                updatedat =field['updatedat']
                if 'linksData' not in field['links']:
                    linkedid = None
                else:
                    linksData_item = field['links']['linksData']['item']
                    if isinstance(linksData_item, list): # Verifica se o item é uma lista
                        linkedid = linksData_item[0]['linkedid']                    
                    else:
                        linkedid = linksData_item['linkedid']
                fields.append(
                    [
                        itemId,
                        taskid,
                        linkedid,
                        title,
                        type,
                        assignee,            
                        priority,
                        subtasks,
                        subtaskscomplete,
                        leadtime,
                        blocked,
                        boardparent,
                        createdat,
                        last_move_time,
                        workflow_id,
                        workflow_name,
                        columnid,
                        columnname,
                        columnpath,
                        laneid,
                        lanename,
                        reporter,
                        logedtime,
                        updatedat,
                        dateHour
                    ]
                )
            try:
                info("Inserido dados do board de id:" + str(itemId) + " dentro do DataFrame")
                df_api = pd.DataFrame(
                    fields,
                    columns=[
                        'boardId',
                        'taskid',
                        'parentid',
                        'title',
                        'type',
                        'assignee',            
                        'priority',
                        'subtasks',
                        'subtaskscomplete',
                        'leadtime',
                        'blocked',
                        'boardparent',
                        'createdat',
                        'last_move_time',
                        'workflow_id',
                        'workflow_name',
                        'columnid',
                        'columnname',
                        'columnpath',
                        'laneid',
                        'lanename',
                        'reporter',
                        'logedtime',
                        'updatedat',
                        'insertDateHour'    
                        ]
                    )
            except:
                error("A quantidade de elementos da lista diverge dos elementos mapeados no dataframe")

        except KeyError:
            debug(xml['xml']['Error'])
            warning("Você não tem permissões para acessar a API do board:"+ str(itemId) + ". Entre em contato com o adm do seu espaço de trabalho")

        df_api['taskid']=df_api['taskid'].astype(int) # tranforma o taskid em inteiro
        df_api['title']=df_api['title'].str.replace('\'','').str.replace('%','pct') # Replace de caracter
        df_api['workflow_name']=df_api['workflow_name'].str.replace('\'','').str.replace('%','pct') # Replace de caracter
                  
    debug(df_api)                
    return df_api