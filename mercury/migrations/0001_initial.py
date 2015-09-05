# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mercury.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('abbreviation', models.CharField(null=True, blank=True, max_length=20)),
                ('name', models.CharField(null=True, blank=True, max_length=100)),
                ('port', mercury.fields.PortField()),
            ],
            options={
                'ordering': ['port', 'protocol'],
            },
        ),
        migrations.CreateModel(
            name='ApplicationPacket',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('src_port', mercury.fields.PortField(verbose_name='SourcePort')),
                ('timestamp', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ApplicationTraffic',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('application', models.ForeignKey(related_name='traffic', to='mercury.Application')),
            ],
            options={
                'ordering': ['application__port'],
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('dns_name', models.CharField(blank=True, max_length=128)),
                ('neighbors', models.ManyToManyField(related_name='neighbors_rel_+', to='mercury.Node')),
            ],
            options={
                'ordering': ['dns_name', 'ip_address'],
            },
        ),
        migrations.CreateModel(
            name='PCAPFile',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('data', models.FileField(upload_to='.')),
                ('processed', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'PCAP Files',
                'verbose_name': 'PCAP File',
            },
        ),
        migrations.CreateModel(
            name='TransportProtocol',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('abbreviation', models.SlugField(unique=True, max_length=10)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='applicationtraffic',
            name='dst_node',
            field=models.ForeignKey(related_name='incoming_traffic', to='mercury.Node', verbose_name='Destination Node'),
        ),
        migrations.AddField(
            model_name='applicationtraffic',
            name='src_node',
            field=models.ForeignKey(related_name='outgoing_traffic', to='mercury.Node', verbose_name='Source Node'),
        ),
        migrations.AddField(
            model_name='applicationpacket',
            name='seen_on',
            field=models.ForeignKey(related_name='packets', to='mercury.Node'),
        ),
        migrations.AddField(
            model_name='applicationpacket',
            name='traffic',
            field=models.ForeignKey(related_name='packets', to='mercury.ApplicationTraffic'),
        ),
        migrations.AddField(
            model_name='application',
            name='protocol',
            field=models.ForeignKey(to='mercury.TransportProtocol'),
        ),
        migrations.AlterUniqueTogether(
            name='applicationtraffic',
            unique_together=set([('application', 'dst_node', 'src_node')]),
        ),
        migrations.AlterUniqueTogether(
            name='application',
            unique_together=set([('port', 'protocol')]),
        ),
    ]
