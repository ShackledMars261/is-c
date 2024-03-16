FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENV RUNNING_IN_DOCKER True

COPY . .

CMD [ "flask", "run", "--host", "0.0.0.0", "--port", "8080" ]