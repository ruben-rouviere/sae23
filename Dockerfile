FROM python:3.10-alpine AS builder

WORKDIR /app

EXPOSE 5000
VOLUME /app/instance

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT ["python3"]
CMD ["-m", "app"]
