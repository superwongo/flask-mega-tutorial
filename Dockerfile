FROM python:3.6-alpine

RUN apk add --no-cache --virtual=build-dependencies \
    g++ \
    build-base libffi-dev python3-dev \
    libffi openssl ca-certificates \
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    linux-headers pcre-dev && \
    adduser -D microblog

WORKDIR /home/microblog

COPY requirements.txt requirements.txt
RUN python -m venv venv && \
#RUN venv/bin/pip install --upgrade pip
    venv/bin/pip install --no-cache-dir -r requirements.txt -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com && \
    venv/bin/pip install --no-cache-dir gunicorn -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com

COPY app app
COPY migrations migrations
COPY microblog.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP microblog.py

RUN chown -R microblog:microblog ./ && \
    rm -rf /root/.cache /home/microblog/.cache
USER microblog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
