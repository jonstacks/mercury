from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from mercury.models import (
    Application,
)

class ApplicationList(ListView):
    context_object_name = 'app_list'
    model = Application
    paginate_by = 50
    template_name = 'mercury/application_list.html'
