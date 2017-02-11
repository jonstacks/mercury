# mercury

A Django Project for understanding your applications through pcap files

## Install

Install requirements with:

    pip install -r requirements/base.txt

Run Migrations:

    ./manage.py migrate

## Usage

Process data from a pcap file with:

    ./manage.py process_pcap <PATH_TO_PCAP_FILE>

Run the server to view the data:

    ./manage.py runserver

## Getting started with Docker

A `Dockerfile` and `docker-compose.yaml` have been included in order to get
up and running faster. This will also help give a consistent development
experience across platforms. To get started, just run

```
docker-compose up -d
```

and open http://localhost in your browser. You will still need to run the
initial migration which you can do by running:

```
docker-compose run --rm mercury manage.py migrate
```
