from django.conf.urls.defaults import *


urlpatterns = patterns('infocomposition.views',
    url(r'^add/$','InfoAdd'),
    url(r'^list/$', 'InfoList'),    
    url(r'^download/(?P<pk>[\d]+)/$','DownloadInfoComp',name='download'),
    url(r'^delete/(?P<pk>[\d]+)/$','DeleteInfoComp', name='delete'),
    url(r'^public/$','PublicList'),
    url(r'^pdownload/(?P<pk>[\d]+)/$','PublicDownload',name='pdownload'),
    url(r'^tags/(?P<tagname>[\w]+)/$','TagsPage',name='tagsrl'),
    url(r'^composition/(?P<pk>[\d]+)/$','CompositionPage',name='compage'),
    url(r'^user_comp/(?P<pk>[\d]+)/$','UserComposition',name='usercomp'),
   
)

