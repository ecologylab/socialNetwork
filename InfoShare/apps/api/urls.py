from django.conf.urls.defaults import *
from piston.resource import Resource
from apps.api.handlers import *
from piston.authentication import HttpBasicCookie
from apps.api.views import InfoCompDownload

auth = HttpBasicCookie()
ad = { 'authentication': auth }

infocomp_handler = Resource(InfoCompositionHandler,**ad)
post_comp = Resource(PostCompositionHandler,**ad)
login_handler = Resource(LoginHandler,**ad)
user_comp = Resource(UserCompositionHandler,**ad)

urlpatterns = patterns('',
   url(r'^get_composition/(?P<hash_key>[\w]+).meta/', infocomp_handler, { 'emitter_format': 'json' }),
   url(r'^get_composition/(?P<hash_key>[\w]+)/', InfoCompDownload),
   url(r'^put_composition/(?P<hash_key>[\w]+)', post_comp, { 'emitter_format': 'json' }),
   url(r'^put_composition/', post_comp, { 'emitter_format': 'json' }),
   url(r'^list_compositions_by_user/(?P<username>[\w]+)', user_comp, { 'emitter_format': 'json' }),
   url(r'^list_compositions_by_user/', user_comp, { 'emitter_format': 'json' }),
   url(r'^login/$',login_handler),
)
