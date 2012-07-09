from django.contrib.auth.models import User
from apps.profiles.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from apps.infocomposition.models import *    
from django.contrib.auth.decorators import login_required 

@login_required
def user_home(request):
    if request.user.is_authenticated():
        tags = Tag.objects.all()
        username = request.user.username
        if(tags):
            tags = Tag.objects.all()[:1].get()
            variables = RequestContext(request,{'username' : username,"tags" : tags})
            return render_to_response('homepage.html', variables)
        else:
            variables = RequestContext(request,{'username' : username,"tags" : tags})
            return render_to_response('homepage.html', variables)

    else:
        return render_to_response('homepage.html',RequestContext(request))


