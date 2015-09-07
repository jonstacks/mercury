from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from mercury.models import (
    Application,
    Node,
)


class ApplicationDetail(DetailView):
    context_object_name = 'app'
    model = Application

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = Node.objects.filter(
            outgoing_traffic__application=context['app'])
        context['servers'] = Node.objects.filter(
            incoming_traffic__application=context['app'])
        return context

    def get_object(self, queryset=None):
        port = self.kwargs['port']
        protocol = self.kwargs['protocol']
        return get_object_or_404(Application, port=port,
                                 protocol__abbreviation=protocol)


class ApplicationList(ListView):
    context_object_name = 'app_list'
    model = Application
    paginate_by = 50


class NodeDetail(DetailView):
    context_object_name = 'node'
    model = Node


class NodeList(ListView):
    context_object_name = 'node_list'
    model = Node
