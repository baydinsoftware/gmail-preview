
from django.conf.urls import patterns, url, include

from preview import views


urlpatterns = patterns('', 
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.detail, name='detail'),
    url(r'^new/$', views.new, name='new'),
)
