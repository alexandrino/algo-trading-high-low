FROM python:3.10-slim

RUN apt-get update && apt-get install -y vim nano procps net-tools

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

CMD ["python", "main.py"]