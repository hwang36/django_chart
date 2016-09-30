from django.conf.urls import patterns, url

from power import views

urlpatterns = patterns('',
    url(r'^summary/(?P<request_date>.+)$', views.view_data, name='viewData'),
)
