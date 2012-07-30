import os
import datetime
from apps.infocomposition.forms import *
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.infocomposition.models import *
from django.http import QueryDict
from django.core.servers.basehttp import FileWrapper
from settings import MEDIA_ROOT

@login_required
def InfoAdd(request):
    """
    Information Composition Main View, To upload Information Composition with related data

    """
    if request.method == 'POST': 
        info_form = InfoForm(request.POST,request.FILES)
        if info_form.is_valid(): 
	    infocomposition = InfoComposition.objects.create(                       
                 name = info_form.cleaned_data['name'],
                 infocomp = request.FILES['infocomp'],
                 description = info_form.cleaned_data['description'],
                 private = info_form.cleaned_data['private'],   
                 user = request.user
               )
            tags_list = info_form.cleaned_data['tags']
            for tag_name in tags_list:                
                tag,created = Tag.objects.get_or_create(tag=tag_name)
                infocomposition.tags.add(tag) 
            return HttpResponseRedirect("/infocomp/add")          
    else:
        info_form = InfoForm()
    variables = RequestContext(request, {'form' : info_form})
    return render_to_response('infocomposition/mainupload.html',variables)
    

    
@login_required
def InfoList(request):
    """
    Listing Information Compositions for current user

    """  
    uid = request.user.id 
    infocomp = InfoComposition.objects.filter(user=uid)
    variables = RequestContext(request, {'infocomps' : infocomp, })
    return render_to_response('infocomposition/infocomplist.html',variables)

@login_required
def DownloadInfoComp(request,pk):
    """
    Download Information Composition .icom file

    """
    infocomposition = InfoComposition.objects.get(pk=pk)
    userid = request.user.id
    infocomp_user = infocomposition.user_id 
    if userid == infocomp_user:
        infocomp = infocomposition.infocomp.name
        infocomp_base = os.path.basename(infocomp)
        file_path = os.path.join(MEDIA_ROOT,infocomp)   
        if os.path.isfile(file_path):     
            wrapper = FileWrapper(open(file_path))  
            response = HttpResponse(wrapper,mimetype='application/force-download')
            response['Content-Length']  = os.path.getsize(file_path)
            response['Content-Disposition'] = "attachment; filename=%s" % infocomp_base
            return response
        else:
            error_message = u"File not found"
            variables = RequestContext(request,{'error_message' : error_message})
            return render_to_response("infocomposition/error.html",variables)
    else:
        error_message = u"Forbidden"
        variables = RequestContext(request, {'error_message' : error_message})
        return render_to_response("infocomposition/error.html",variables)

           
    
   
@login_required
def DeleteInfoComp(request,pk):
    """
    Delete Information Composition
    
    """
  
    infocomposition = InfoComposition.objects.get(pk=pk)
    userid = request.user.id
    username = request.user.username
    infocomp_user = infocomposition.user_id
    if userid == infocomp_user:
        name = infocomposition.name
        infocomposition.delete()   
        return HttpResponseRedirect("/infocomp/list")
    else: 
        error_message = u"Forbidden"
        variables = RequestContext(request, {'error_message' : error_message})
        return render_to_response("infocomposition/error.html",variables) 
    

def PublicList(request):
    """
    Public List of Information Compositions

    """
    infocomposition = InfoComposition.objects.filter(private=False) 
    variables = RequestContext(request,{'infocomps' : infocomposition})
    return render_to_response("infocomposition/publiclist.html",variables)

def PublicDownload(request,pk):
    """
    Public Download Option, Without checking whether user owns information composition or not

    """
    infocomposition = InfoComposition.objects.get(pk=pk)
    infocomp = infocomposition.infocomp.name
    infocomp_base = os.path.basename(infocomp)
    file_path = os.path.join(MEDIA_ROOT,infocomp)   
    if os.path.isfile(file_path):     
        wrapper = FileWrapper(open(file_path))  
        response = HttpResponse(wrapper,mimetype='application/force-download')
        response['Content-Length']  = os.path.getsize(file_path)
        response['Content-Disposition'] = "attachment; filename=%s" % infocomp_base
        return response
    else:
        error_message = u"File not found"
        variables = RequestContext(request,{'error_message' : error_message})
        return render_to_response("infocomposition/error.html",variables)
    
@login_required
def CompositionPage(request,pk):
    """
    Information Composition Page

    """
    infocomp = InfoComposition.objects.get(pk=pk)
    if request.method == "POST":
        comment = Comment(
            infocomp = infocomp,
            author=request.user.username,
            comment=request.POST['comment'],
            added=datetime.datetime.now(),
        )
       # if this is a reply to a comment, not to a post
        if request.POST['parent_id'] != '':
            comment.parent = Comment.objects.get(id=request.POST['parent_id'])
        comment.save()
    comments = Comment.objects.filter(infocomp=infocomp)
    variables = RequestContext(request, {'infocomp' : infocomp,'comments' : comments })
    return render_to_response("infocomposition/infocomposition.html",variables)

@login_required
def UserComposition(request,pk):
    """
    Information Compositions by specific user

    """
    user = User.objects.get(pk=pk)
    user_id = user.id  
    username = user.username
    infocomp = InfoComposition.objects.filter(user=user_id,private=False)
    variables = RequestContext(request,{'infocomps' : infocomp,'username' : username})
    return render_to_response("infocomposition/infouser.html",variables)

@login_required
def TagsPage(request,tagname):
    """
    Tags Page

    """
    user_id = request.user.id  
    tag = get_object_or_404(Tag,tag=tagname)
    public_infocomps = InfoComposition.objects.filter(tags=tag,private=False)
    user_infocomps = InfoComposition.objects.filter(tags=tag,user=user_id)
    infocomps = public_infocomps | user_infocomps
    infocomps = infocomps.order_by("added")
    variables = RequestContext(request, {'infocomps' : infocomps,'tagname' : tagname})
    return render_to_response("infocomposition/tags.html",variables) 



