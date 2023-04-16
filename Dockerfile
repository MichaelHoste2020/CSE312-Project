FROM python:3.9

ENV HOME /root

WORKDIR /root

COPY . .

RUN pip install uvicorn[standard]
RUN pip install fastapi
RUN pip install pymongo
RUN pip install pydantic
RUN pip install python-multipart

EXPOSE 8000

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && python -u server.py