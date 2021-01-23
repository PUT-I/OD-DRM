FROM python:3.7

WORKDIR ./app/

COPY ./src/ ./src/
COPY ./requirements.txt ./requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app/src/"
RUN pip install -r requirements.txt

EXPOSE 5001

RUN "python" "./src/orm_objects.py"
ENTRYPOINT ["python", "./src/main.py"]
