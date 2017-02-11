FROM python:3.6-alpine

# For scapy
RUN apk add --no-cache alpine-sdk postgresql-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements /usr/src/app/requirements
RUN pip install --no-cache-dir -r requirements/production.txt

COPY . /usr/src/app

EXPOSE 80
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:80"]
