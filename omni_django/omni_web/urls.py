from django.conf.urls import patterns, url
from omni_web import views

urlpatterns = patterns('',
                       url(r'^$', views.main, name='main'),
                       url(r'route', views.route, name='route'),)
#url(r'^$',views.routes, name='route-mockup')
