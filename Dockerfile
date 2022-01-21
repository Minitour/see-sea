FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./start.sh /code/start.sh

RUN chmod +x /code/start.sh
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./sea /code/sea

CMD ["./start.sh"]

