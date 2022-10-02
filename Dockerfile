FROM python:3.9-slim

LABEL maintainer="rafael.bomfim@primecontrol.com.br"

WORKDIR /usr/src/app
COPY requirements.txt ./

ARG TZ="America/Sao_Paulo"
ENV TZ ${TZ}

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3"]