FROM python:3.6-alpine

RUN apk add --no-cache --virtual=build-dependencies g++ zlib-dev jpeg-dev && \
    adduser -D microblog

WORKDIR /home/microblog

COPY requirements.txt requirements.txt
RUN python -m venv venv && \
    venv/bin/pip install --no-cache-dir -r requirements.txt -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com && \
    venv/bin/pip install --no-cache-dir gunicorn pymysql -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com

COPY app app
COPY migrations migrations
COPY microblog.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP microblog.py

RUN chown -R microblog:microblog ./
USER microblog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
