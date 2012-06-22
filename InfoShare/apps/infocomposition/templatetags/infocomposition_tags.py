import os
from apps.infocomposition.models import *
from django.contrib.auth.models import User
from django.template import Library
from settings import MEDIA_URL
register = Library()

@register.simple_tag
def media_url():
    return MEDIA_URL

@register.simple_tag
def get_html_path(user,pk):
    user_id = user
    user_object = User.objects.get(pk=user_id)
    username = user_object.username
    infocomposition = InfoComposition.objects.get(pk=pk)
    infocomp_name = infocomposition.infocomp.name
    infocomp_with_ext = os.path.basename(infocomp_name)
    infocomp_file = os.path.splitext(infocomp_with_ext)[0]
    html_name = infocomp_file + ".html"
    html_path = os.path.join(MEDIA_URL,"infocomp",username,infocomp_file,html_name)
    return html_path 
