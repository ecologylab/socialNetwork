import os
from shutil import rmtree
from apps.infocomposition.forms import *
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from apps.infocomposition.models import *
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
            tags_list = tags_list.split(",")
            for tag_name in tags_list:                
                tag,created = Tag.objects.get_or_create(tag=tag_name)
                infocomposition.tags.add(tag) 
            infocomposition.save()
            infocomposition.unzip_icom()
            infocomposition.add_filename()
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
    infocomp = infocomposition.infocomp.name
    infocomp_base = os.path.basename(infocomp)
    username = request.user.username
    file_path = os.path.join(MEDIA_ROOT,"infocomp",username,infocomp_base)   
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
        infocomp_name = infocomposition.infocomp.name
        infocomp_with_ext = os.path.basename(infocomp_name)
        infocomp_file = os.path.splitext(infocomp_with_ext)[0]
        infocomp_path = os.path.join(MEDIA_ROOT,infocomp_name)  
        infocomp_dirpath = os.path.join(MEDIA_ROOT,"infocomp",username,infocomp_file)        
        if os.path.isfile(infocomp_path):
            os.remove(infocomp_path)
        if os.path.isdir(infocomp_dirpath): 
            rmtree(infocomp_dirpath)
        infocomposition.delete()
        success_message = u"You have successfully removed information compostion %s" % name     
        return HttpResponseRedirect("/infocomp/list")
    else: 
        error_message = u"You don't own this information composition, hence can not be deleted"
        variables = RequestContext(request, {'error_message' : error_message})
        return render_to_response("infocomposition/error.html",variables) 
    
 



