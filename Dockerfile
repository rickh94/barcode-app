FROM python:3.9

RUN pip install pipenv
RUN pip install gunicorn

ADD ./Pipfile .
ADD ./Pipfile.lock .
RUN pipenv install --system --deploy

ADD ./app /app/app
RUN ARCH=`uname -m` && \
    curl -L -o /app/app/barcode.so \
    "https://github.com/rickh94/barcode_generator/releases/download/v21.01.1/barcode-$ARCH.so"
WORKDIR /app/app
RUN mkdir /output

CMD gunicorn -w4 -b "$HOST:$PORT" main:app
