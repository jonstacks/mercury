import argparse

from django.core.management.base import BaseCommand

from scapy.all import rdpcap
from scapy.layers.dns import DNS, dnstypes
from scapy.layers.inet import IP, TCP

from mercury.models import PCAPFile, Node, Application, ApplicationTraffic, TransportProtocol
from mercury.utils import is_tcp_handshake_start

def reverse_octets(ip_address):
    octets = ip_address.split('.')
    octets.reverse()
    return '.'.join(octets)

class Command(BaseCommand):
    help = 'Processes a given pcap file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=argparse.FileType('r'))

    def handle(self, *args, **options):
        print(options['file'].name)
        self.packets = rdpcap(options['file'].name)
        self.parse_dns_entries()
        self.parse_client_server_traffic()

    def parse_dns_entries(self):
        print('Showing DNS Queries...')
        dns_packets = filter(lambda x: DNS in x, self.packets)
        for p in dns_packets:
            dns_an = p[DNS].an
            if dns_an is None:
                continue

            if dnstypes[dns_an.type] == 'A':
                ip = dns_an.rdata
                name = dns_an.rrname.decode('utf-8').rstrip('.')
            elif dnstypes[dns_an.type] == 'PTR':
                ip = dns_an.rrname.decode('utf-8')
                ip = reverse_octets(ip.rstrip('.in-addr.arpa.'))
                name = dns_an.rdata.decode('utf-8').rstrip('.')
            else:
                continue

            n, create = Node.objects.get_or_create(ip_address=ip)
            n.dns_name = name
            n.save()

    def parse_client_server_traffic(self):
        print('Parsing Client-Server communication...')
        self.parse_client_server_tcp_traffic()

    def parse_client_server_tcp_traffic(self):
        protocol, created = TransportProtocol.objects.get_or_create(
            abbreviation='TCP', name='Transmission Control Protocol')
        tcp_packets = filter(lambda x: TCP in x, self.packets)
        for p in tcp_packets:
            if is_tcp_handshake_start(p[TCP].flags):
                dst_node, created = Node.objects.get_or_create(ip_address=p[IP].dst)
                src_node, created = Node.objects.get_or_create(ip_address=p[IP].src)
                app, created = Application.objects.get_or_create(
                    port=p[TCP].dport, protocol=protocol)
                traffic, created = ApplicationTraffic.objects.get_or_create(
                    application=app, dst_node=dst_node, src_node=src_node)
