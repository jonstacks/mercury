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


class NodeAdmin(admin.ModelAdmin):
    list_display = ('dns_name', 'ip_address', )


admin.site.register(Application)
admin.site.register(ApplicationPacket)
admin.site.register(ApplicationTraffic)
admin.site.register(Node, NodeAdmin)
admin.site.register(PCAPFile, FileAdmin)
admin.site.register(TransportProtocol)
