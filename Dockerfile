FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./CompassUTD /app/CompassUTD

RUN ls --recursive /app/CompassUTD

COPY ./fast_api_app /app

