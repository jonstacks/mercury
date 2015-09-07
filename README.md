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
