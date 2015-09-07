import csv
import os

from django.core.management.base import BaseCommand

from mercury.models import Application, TransportProtocol


class Command(BaseCommand):
    help = 'Loads application and transport definitions'

    def handle(self, *args, **options):
        x = os.path.dirname(__file__)
        definition_dir = os.path.join(x, '../../data/definitions')
        with open(os.path.join(definition_dir, 'protocols.csv')) as csvfile:
            protocols = csv.reader(csvfile)
            next(protocols) # Ignore heading
            for (abbreviation, name) in protocols:
                protocol, created = TransportProtocol.objects.get_or_create(
                    abbreviation=abbreviation)
                protocol.name = name
                protocol.save()
                if created:
                    print("Created new Protocol: {}".format(abbreviation))

        with open(os.path.join(definition_dir, 'ports.csv')) as csvfile:
            applications = csv.reader(csvfile)
            next(applications) # Ignore heading
            for (port, protocols, name, abbreviation) in applications:
                protocols = protocols.split(',')
                for protocol in protocols:
                    p = TransportProtocol.objects.get(abbreviation=protocol)
                    app, created = Application.objects.get_or_create(
                        port=port, protocol= p)
                    app.name = name
                    app.abbreviation = abbreviation
                    app.save()
                    if created:
                        print("Created new App: {}".format(app.name))
