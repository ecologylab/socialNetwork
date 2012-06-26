import os
import glob
from apps.infocomposition.models import *
from django.contrib.auth.models import User
from django.template import Library
from settings import MEDIA_URL, MEDIA_ROOT
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
    dir_path = os.path.splitext(infocomp_name)[0]
    infocomp_dir = os.path.join(MEDIA_ROOT,dir_path)
    infocomp_with_ext = os.path.basename(infocomp_name)
    infocomp_file = os.path.splitext(infocomp_with_ext)[0]
    os.chdir(infocomp_dir)
    file_list =  glob.glob("*.html")
    length = len(file_list)
    if length > 1:
        for name in file_list:
            if name.startswith(infocomp_file):
                html_name = name
                html_path = os.path.join(MEDIA_URL,"infocomp",username,infocomp_file,html_name)
                return html_path
            else:
                return "#"
    elif length < 1:
        return '#'
    else:
        html_path = os.path.join(MEDIA_URL,"infocomp",username,infocomp_file,file_list[0])
        return html_path 
      

@register.simple_tag
def get_user_name(pk):
    user = User.objects.get(pk=pk)
    username = user.username
    return username


