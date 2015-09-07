import argparse

from django.core.management.base import BaseCommand

from scapy.utils import PcapReader
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
        packet_count = 0
        self.tcp, created = TransportProtocol.objects.get_or_create(
            abbreviation='TCP', name='Transmission Control Protocol')

        with PcapReader(options['file'].name) as pcap_reader:
            for pkt in pcap_reader:
                if DNS in pkt:
                    print(repr(pkt))
                    self.process_dns_packet(pkt)
                    print('Processed DNS packet.')
                elif TCP in pkt:
                    self.process_client_server_tcp_packet(pkt)
                    print('Processed TCP packet.')
                packet_count += 1

        print("Processed {} packets".format(packet_count))

    def process_dns_packet(self, p):
        dns_an = p[DNS].an
        if dns_an is None:
            return
        if dnstypes[dns_an.type] == 'A':
            ip = dns_an.rdata
            name = dns_an.rrname.decode('utf-8').rstrip('.')
        elif dnstypes[dns_an.type] == 'PTR':
            ip = dns_an.rrname.decode('utf-8')
            ip = reverse_octets(ip.rstrip('.in-addr.arpa.'))
            name = dns_an.rdata.decode('utf-8').rstrip('.')
        else:
            return

        n, create = Node.objects.get_or_create(ip_address=ip)
        n.dns_name = name
        n.save()

    def process_client_server_tcp_packet(self, p):
        if is_tcp_handshake_start(p[TCP].flags):
            dst_node, created = Node.objects.get_or_create(ip_address=p[IP].dst)
            src_node, created = Node.objects.get_or_create(ip_address=p[IP].src)
            app, created = Application.objects.get_or_create(
                port=p[TCP].dport, protocol=self.tcp)
            traffic, created = ApplicationTraffic.objects.get_or_create(
                application=app, dst_node=dst_node, src_node=src_node)
