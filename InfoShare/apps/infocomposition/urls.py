from django.conf.urls.defaults import *



urlpatterns = patterns('infocomposition.views',
    url(r'^add/$','InfoAdd', name="addinfocomp"),
    url(r'^list/$', 'InfoList', name="mylistcomp"),    
    url(r'^download/(?P<hash_key>[\w]+)/$','DownloadInfoComp',name='download'),
    url(r'^delete/(?P<hash_key>[\w]+)/$','DeleteInfoComp', name='delete'),
    url(r'^public/$','PublicList',name="publiclist"),
    url(r'^tags/(?P<tagname>[\w]+)/$','TagsPage',name='tagsrl'),
    url(r'^c/(?P<hash_key>[\w]+)/$','CompositionPage',name='compage'),
    url(r'^user_comp/(?P<pk>[\d]+)/$','UserComposition',name='usercomp'),
    url(r'^html5/(?P<hash_key>[\w]+)/$','HTML5View',name='full_view')    
)

