FROM python:slim

RUN useradd liftzoid

WORKDIR /home/liftzoid

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql cryptography

COPY app app
COPY migrations migrations
COPY liftzoid.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP liftzoid.py

RUN chown -R liftzoid:liftzoid ./
USER liftzoid

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
