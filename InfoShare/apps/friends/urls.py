from django.conf.urls.defaults import *


urlpatterns = patterns('friends.views',
    url(r'^$','list_friends',name='friends_friends'),
    url(r'^invite/(?P<username>[\.\w]+)/$','invite_friend', name='friends_invite'),
    url(r'^remove/(?P<username>[\.\w]+)/$','remove_friend', name='friends_remove'),
    url(r'^block/(?P<username>[\.\w]+)/$','block_user', name='friends_block_user'),
    url(r'^unblock/(?P<username>[\.\w]+)/$','unblock_user',name='friends_unblock_user'),
    url(r'^blocked/$','list_blocked_users',name='friends_blocked_users'),
    url(r'^invitations/received/$','list_received_invitations',name='friends_received_invitations'),
    url(r'^invitations/sent/$','list_sent_invitations',name='friends_sent_invitations'),
    url(r'^invitation/(?P<invitation_id>[\d]+)/$','show_invitation',name='friends_show_invitation'),
    url(r'^invitation/(?P<invitation_id>[\d]+)/remove/$','remove_invitation',name='friends_remove_invitation'),
    url(r'^invitation/(?P<invitation_id>[\d]+)/accept/$','respond_to_invitation',{'resp': 'a'}, name='friends_accept_invitation'),
    url(r'^invitation/(?P<invitation_id>[\d]+)/decline/$','respond_to_invitation',{'resp': 'd'}, name='friends_decline_invitation'),
    url(r'^of_friend/(?P<username>[\.\w]+)/$','list_friend_friends',name='friends_friend_friends'),


)

