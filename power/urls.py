from django.conf.urls import patterns, url

from power import views

urlpatterns = patterns('',
    url(r'^summary$', views.view_data, name='viewData'),
    url(r'^$', views.index, name='index'),

)