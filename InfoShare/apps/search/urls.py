from django.conf.urls.defaults import *


urlpatterns = patterns('search.views',
    url(r'^$','search_list',name='search_list'),  
    
    
)

