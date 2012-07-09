import os
import glob
from datetime import datetime
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
def get_human_time(time):
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time 
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"

