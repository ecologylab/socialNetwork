from django.conf.urls.defaults import *


urlpatterns = patterns('infocomposition.views',
    url(r'^add/$','InfoAdd'),
    url(r'^list/$', 'InfoList'),    
    url(r'^download/(?P<pk>[\d]+)/$','DownloadInfoComp',name='download'),
    url(r'^delete/(?P<pk>[\d]+)/$','DeleteInfoComp', name='delete'),

)

