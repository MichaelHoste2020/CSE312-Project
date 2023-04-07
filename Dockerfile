FROM python:3.9

ENV HOME /root

WORKDIR /root

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]