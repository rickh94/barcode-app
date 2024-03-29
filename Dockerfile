FROM python:3.9

RUN pip install gunicorn

ADD ./requirements.txt .
RUN pip install -r requirements.txt

ADD ./app /app/app
RUN ARCH=`uname -m` && \
    curl -L -o /app/app/barcode.so \
    "https://github.com/rickh94/barcode_generator/releases/download/v21.01.1/barcode-$ARCH.so"
WORKDIR /app/app
RUN mkdir /output

CMD gunicorn -w4 -b "$HOST:$PORT" main:app
