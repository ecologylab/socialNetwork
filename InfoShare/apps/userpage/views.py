from django.contrib.auth.models import User
from apps.profiles.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response


def user_home(request):
    if request.user.is_authenticated():
        username = request.user.username
        uid = request.user.id
        email = request.user.email
        user_pro = Profile.objects.get(user=uid)
        variables = RequestContext(request,{'username' : username,"email" : email})
        return render_to_response('homepage.html', variables)
    else:
        return render_to_response('homepage.html',RequestContext(request))
 
