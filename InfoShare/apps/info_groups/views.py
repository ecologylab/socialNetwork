from apps.info_groups.models import *
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.info_groups.forms import GroupForm

@login_required
def CreateGroup(request):
    """ Create Group Form View """
   
    if request.method == 'POST': 
        group_form = GroupForm(request.POST)
        if group_form.is_valid():
            group_obj = Group.objects.create(
                        name=group_form.cleaned_data['name'],
                        privacy=group_form.cleaned_data['privacy']
                        )
            group_obj.add_user(request.user,is_admin=True)       
    else:
        group_form = GroupForm()
    variables = RequestContext(request, {'form' : group_form})
    return render_to_response('groups/create.html',variables)

@login_required
def ListGroups(request):
   """ View list of groups """

   group_open = Group.objects.filter(privacy='0')
   group_closed = Group.objects.filter(privacy='1')
   groups = group_open | group_closed
   variables = RequestContext(request, {'groups' : groups})
   return render_to_response('groups/list.html',variables)

@login_required
def GroupDetail(request,hash_key):
   """ View for the page that contain all details of the particular group """
   
   group_name = get_object_or_404(Group,hash_key=hash_key)
   variables = RequestContext(request, {'form' : 1,'group' : group_name})
   return render_to_response('groups/detail.html',variables)

@login_required
def MembersList(request,hash_key):
    """ This view returns list of members for particular group """

    group_name = get_object_or_404(Group,hash_key=hash_key)
    members = group_name.users.all()
    variables = RequestContext(request, {'name' : group_name,'members' : members})         
    return render_to_response('groups/members.html',variables)    

