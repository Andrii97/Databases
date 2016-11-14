from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list/$', views.listView),
    url(r'^init/$', views.initializeDatabase),
    url(r'^add/$', views.addCompetition),
    url(r'^aggregate/$', views.aggregateAndMapReduce),
    url(r'^remove/(?P<id>[a-zA-Z0-9]+)$', views.removeCompetition),
    url(r'^(?P<id>[a-zA-Z0-9]+)$', views.editCompetition)
    # ^(?P<id>[0-9]+)$
]