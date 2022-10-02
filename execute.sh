#!/bin/bash
#
# Comandos para executar imagem em container
dir=$(pwd)

echo Executando extrator em container
docker run ^
--rm ^
--volume $dir:/usr/src/app ^
-w /usr/src/app ^
--name kanbanize_extrator ^
kanbanize_extrator:2.0-filter ^
python main.py