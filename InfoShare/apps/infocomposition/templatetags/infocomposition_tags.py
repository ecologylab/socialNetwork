from django.template import Library
from settings import MEDIA_URL
register = Library()

@register.simple_tag
def media_url():
    return MEDIA_URL

def get_thumbnail_path(user,name):
    pass
