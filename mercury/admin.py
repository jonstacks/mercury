from django.contrib import admin

from mercury.models import (
    Application,
    ApplicationPacket,
    ApplicationTraffic,
    Node,
    PCAPFile,
    TransportProtocol
)


class FileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'processed', )
    list_filter = ('processed', )
    readonly_fields = ('processed', )

admin.site.register(Application)
admin.site.register(ApplicationPacket)
admin.site.register(ApplicationTraffic)
admin.site.register(Node)
admin.site.register(PCAPFile, FileAdmin)
admin.site.register(TransportProtocol)
