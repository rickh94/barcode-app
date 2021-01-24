ARG ARCH=
FROM ${ARCH}python:3.9

RUN pip install pipenv
RUN pip install gunicorn

ADD ./Pipfile .
ADD ./Pipfile.lock .
RUN pipenv install --system --deploy

ADD ./app /app/app
WORKDIR /app/app
RUN mkdir /output

CMD gunicorn -w4 -b "$HOST:$PORT" main:app
