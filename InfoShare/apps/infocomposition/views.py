import os
import glob
import datetime
from apps.infocomposition.forms import *
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.infocomposition.models import *
from django.http import QueryDict
from django.core.servers.basehttp import FileWrapper
from settings import MEDIA_ROOT, MEDIA_URL

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
            return HttpResponseRedirect("/ic/add")          
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
def DownloadInfoComp(request,hash_key):
    """
    Download Information Composition .icom file

    """
    infocomposition = get_object_or_404(InfoComposition,hash_key=hash_key)
    userid = request.user.id
    infocomp_user = infocomposition.user_id 
    if userid == infocomp_user or infocomposition.private == False:
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
def DeleteInfoComp(request,hash_key):
    """
    Delete Information Composition
    
    """
  
    infocomposition = get_object_or_404(InfoComposition,hash_key=hash_key)
    userid = request.user.id
    username = request.user.username
    infocomp_user = infocomposition.user_id
    if userid == infocomp_user:
        name = infocomposition.name
        infocomposition.delete()   
        return HttpResponseRedirect("/ic/list")
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

   
@login_required
def CompositionPage(request,hash_key):
    """
    Information Composition Page

    """
    infocomp = get_object_or_404(InfoComposition,hash_key=hash_key)
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


@login_required
def HTML5View(request,hash_key):
    """
    To view HTML5 enabled information composition

    """
    infocomposition = get_object_or_404(InfoComposition,hash_key=hash_key)
    user_id = request.user.id
    infocomp_user = infocomposition.user
    if infocomposition.private == True and infocomp_user.id != user_id:
        response = HttpResponse("This information composition is private and you are not owner of it.")
        response.status_code = 404
        return response        
    else:
        infocomp_name = infocomposition.infocomp.name
        dir_path = os.path.splitext(infocomp_name)[0]
        infocomp_dir = os.path.join(MEDIA_ROOT,dir_path)
        os.chdir(infocomp_dir)
        file_list =  glob.glob("*.json")
        if len(file_list) == 0:
            error_message = u"This Information composition doesn't support this view"
            variables = RequestContext(request,{'error_message' : error_message})
            return render_to_response("infocomposition/error.html",variables)
        else:
            infocomp_with_ext = os.path.basename(infocomp_name)
            infocomp_file = os.path.splitext(infocomp_with_ext)[0]
            file_name = file_list[0]
            username = infocomposition.user.username          
            file_path = os.path.join(MEDIA_ROOT,"infocomp",username,infocomp_file,file_name)
            json_file = open(file_path,'r')
            json_data = json_file.read()
            infocomp_main_name = infocomposition.name
            variables = RequestContext(request, {'name' : infocomp_main_name,'json_data':json_data})      
            return render_to_response("infocomposition/full.html",variables)
