FROM debian:stretch

RUN apt-get update && apt-get install -y python3 python3-pip uwsgi uwsgi-plugin-python3 && \
     useradd docker && mkdir -p /srv/app/cache && chown docker:docker /srv/app/cache

COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

COPY app.py /srv/app/app.py

ENV prometheus_multiproc_dir /srv/app/cache

EXPOSE 6543 
WORKDIR /srv/app
USER docker
CMD uwsgi --master --plugin python35 --processes 2 --http-socket 0.0.0.0:6543 --wsgi-file  /srv/app/app.py
