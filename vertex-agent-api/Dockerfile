FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./requirements.txt /app/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


ENV NLTK_DATA=/

RUN python -m textblob.download_corpora


COPY ./app /app

