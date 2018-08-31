FROM python:3.6

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY ./conf/django/dev/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
