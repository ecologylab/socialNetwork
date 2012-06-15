from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from apps.userpage.views import *
from django.contrib import admin
admin.autodiscover()
import os
from pinax.apps.account.openid_consumer import PinaxConsumer
static = os.path.join(os.path.dirname(__file__),"site_media","static")
media = os.path.join(os.path.dirname(__file__),"site_media","media")

handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", user_home, name="home"),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r'^friends/', include('friends.urls')),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^avatar_crop/', include('avatar_crop.urls')),
    url(r"^announcements/", include("announcements.urls")),
    url(r"^messages/", include('messages.urls')),
    
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': static}),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': media}),
    )
