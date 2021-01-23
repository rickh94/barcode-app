FROM python:3.9

RUN pip install pipenv
RUN pip install gunicorn

RUN apt-get update -y
RUN apt-get install -y ghostscript

ADD ./Pipfile .
ADD ./Pipfile.lock .
RUN pipenv install --system --deploy

ADD ./app /app/app
WORKDIR /app/app
RUN mkdir /output

CMD gunicorn -w4 -b "$HOST:$PORT" main:app