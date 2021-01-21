FROM python:3.7.9

RUN apt update && \
    apt install -y redis-server && \
    git clone https://github.com/deepmipt/EasyIntentCacther && \
    cd EasyIntentCacther && \
    pip install -r requirements.txt && \
    python manage.py migrate && \
    mkdir logs

WORKDIR /EasyIntentCacther

CMD redis-server > redis.log 2>&1 & \
    celery  -A EasyIntentCatcher worker -l INFO > celery.log 2>&1 & \
    python manage.py runserver 0.0.0.0:8000