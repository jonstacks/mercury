import uuid

from django.db import models
from hurry.filesize import size

from mercury.fields import PortField


class Application(models.Model):
    """Class to map well known ports to an Application."""

    class Meta:
        ordering = ['port', 'protocol']
        unique_together = (('port', 'protocol'), )

    abbreviation = models.CharField(blank=True, max_length=20, null=True)
    name = models.CharField(blank=True, max_length=100, null=True)
    port = PortField()
    protocol = models.ForeignKey('TransportProtocol')

    def __str__(self):
        if self.abbreviation:
            return self.abbreviation
        if self.name:
            return self.name
        return str(self.port)


class ApplicationTraffic(models.Model):
    """Class for traffic that defines an application."""

    class Meta:
        ordering = ['application__port', ]
        unique_together = (('application', 'dst_node', 'src_node', ), )

    application = models.ForeignKey(Application, related_name='traffic')
    dst_node = models.ForeignKey('Node', related_name='incoming_traffic',
                                 verbose_name='Destination Node')
    src_node = models.ForeignKey('Node', related_name='outgoing_traffic',
                                 verbose_name='Source Node')

    def __str__(self):
        return "{s_node} -> {d_node} [{app}]".format(app=self.application,
                                                     d_node=self.dst_node,
                                                     s_node=self.src_node)


class ApplicationPacket(models.Model):
    """
    Class to hold the node the application traffic was gathered on and at what
    time. Represents the varrying parts of Application Traffic gathered in a
    network.
    """

    class Meta:
        ordering = ['timestamp', ]

    seen_on = models.ForeignKey('Node', related_name='packets')
    src_port = PortField(verbose_name='SourcePort')
    timestamp = models.DateTimeField(blank=True, null=True)
    traffic = models.ForeignKey(ApplicationTraffic, related_name='packets')


class Node(models.Model):
    """A generic node in the network. """

    class Meta:
        ordering = ['dns_name', 'ip_address', ]

    ip_address = models.GenericIPAddressField()
    dns_name = models.CharField(blank=True, max_length=128)
    neighbors = models.ManyToManyField('self')

    def __str__(self):
        return self.dns_name if self.dns_name else self.ip_address


class PCAPFile(models.Model):
    """A PCAP File that stores the raw data we need to process. """

    class Meta:
        verbose_name = 'PCAP File'
        verbose_name_plural = 'PCAP Files'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = models.FileField(upload_to='.')
    processed = models.BooleanField(default=False)

    def __str__(self):
        return "{0} ({1})".format(self.data.name, size(self.data.size))


class TransportProtocol(models.Model):
    """A Transport Layer Protocol."""

    abbreviation = models.SlugField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.abbreviation
