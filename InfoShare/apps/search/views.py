from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from apps.infocomposition.models import *
from haystack.query import SearchQuerySet

@login_required
def search_list(request):
    try:
        sTerm = request.GET['q']
    except:
        return HttpResponseRedirect('/')
    results = SearchQuerySet().auto_query(sTerm)
    search_infocomp = []
    search_user = []
    InfoComp = []

    for result in results:
        if str(result.model_name) == "user":
            search_user.append(result.object)
        else:
            search_infocomp.append(result.object)

    for result in search_infocomp: 
        if result.private == True:
            if result.user_id == request.user.id:
                InfoComp.append(result)        
        else: 
            InfoComp.append(result)
         
    variables = RequestContext(request,{'infocomps' : InfoComp,"users" : search_user  })
    return render_to_response("search/search.html",variables)
