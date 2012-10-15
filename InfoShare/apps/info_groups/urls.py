from django.conf.urls.defaults import *



urlpatterns = patterns('info_groups.views',
    url(r'^$','ListGroups', name="list_groups"),
    url(r'^create/$', 'CreateGroup', name="create_group"),    
    url(r'^group/(?P<hash_key>[\w]+)/$','GroupDetail',name='detail_group'),       
    url(r'^members/(?P<hash_key>[\w]+)/$','MembersList',name='members_list'),
 
)


