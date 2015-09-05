from django.db import models
from django.utils.translation import ugettext_lazy as _


class PortField(models.PositiveIntegerField):
    description = _("Networking Packet Port Field")
    MAX_PORT = 65535

    def formfield(self, **kwargs):
        defaults = {'max_value': PortField.MAX_PORT}
        defaults.update(kwargs)
        return super(PortField, self).formfield(**defaults)
