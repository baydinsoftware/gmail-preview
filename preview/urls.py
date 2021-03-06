
from django.conf.urls import patterns, url, include

from preview import views

urlpatterns = patterns('', 
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.detail, name='detail'),
    url(r'^new/$', views.new, name='new'),
    url(r'^login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'preview/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', 
        {'template_name': 'preview/logout.html'}, name='logout'),
    url(r'^reset/$', 'django.contrib.auth.views.password_reset', 
        {'template_name': 'preview/reset.html'}, name='reset'),
    url(r'^register/$', views.register, name='register'),
)
