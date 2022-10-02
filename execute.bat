@echo off
echo Executando extrator em container
docker run ^
--rm ^
--volume %CD%:/usr/src/app ^
-w /usr/src/app ^
--name kanbanize_extrator ^
kanbanize_extrator:2.0-filter ^
python main.py