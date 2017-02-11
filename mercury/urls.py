"""mercury URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from mercury.views import (
    ApplicationDetail,
    ApplicationList,
    NodeDetail,
    NodeList,
    TrafficMap,
    application_traffic,
)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^app/$', ApplicationList.as_view(), name='app-list'),
    url(r'^app/(?P<protocol>\w+)/(?P<port>\d+)/$', ApplicationDetail.as_view(),
        name='app-detail'),
    url(r'^nodes/$', NodeList.as_view(), name='node-list'),
    url(r'^nodes/(?P<pk>\d+)/$', NodeDetail.as_view(), name='node-detail'),
    url(r'^traffic/map/$', TrafficMap.as_view(), name='traffic-map'),

    url(r'^api/app-traffic/$', application_traffic),
    url(r'^$', RedirectView.as_view(url='app', permanent=False), name='index'),
]
