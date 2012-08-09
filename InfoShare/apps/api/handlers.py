import os
from piston.handler import BaseHandler
from apps.infocomposition.models import *
from django.shortcuts import get_object_or_404
from apps.api.utils import GetDict, UserDict
from piston.utils import rc
from apps.infocomposition.models import InfoComposition
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import datetime

class InfoCompositionHandler(BaseHandler):
   allowed_methods = ('GET',)

   def read(self,request,hash_key=None):
       
       if hash_key:
           cur_obj = get_object_or_404(InfoComposition,hash_key=hash_key)
           user_id = int(cur_obj.user.id)
           
           if cur_obj.private == True:
               if int(request.user.id) == user_id:
                   return GetDict(cur_obj)
               else:
                   response = rc.FORBIDDEN
                   return response
           else:
               return GetDict(cur_obj)
             
                                         
class PostCompositionHandler(BaseHandler):
    allowed_methods = ('POST',)
    model = InfoComposition    
  
      
    def create(self,request,hash_key=None):  
        if hash_key:
            data = request.data
            infocomp = get_object_or_404(InfoComposition,hash_key=hash_key)
            userid = request.session['_auth_user_id']           
            if infocomp.user.id == userid:
                if 'name' in data:
                    infocomp.name = data['name']
                if 'description' in data: 
                    infocomp.description = data['description']
                if 'private' in data:
                    if data['private'] == True:
                        infocomp.private = True
                    else:
                        infcomp.private = False
                if 'infocomp' in request.FILES:
                     infocomp_file = request.FILES["infocomp"]
                     infocomp_filename = infocomp_file.name
                     ext = os.path.splitext(infocomp_filename)[1]
                     ext = ext.lower()
                     if not ext == ".icom":
                         response = rc.BAD_REQUEST
                         response.write(", Please upload information Composition file, It should have icom extension")
                         return response
                     infocomp.delete_related_data()
                     infocomp.infocomp = infocomp_file
                if 'tags' in data:
                    tags = data["tags"]
                    tags_list = tags.split(",")
                    tags_final = []
                    for tag in tags_list:
                        tag = tag.lower().strip()
                        tag = slugify(tag)
                        tag = tag.replace("-","_")
                        tags_final.append(tag)
                    for tag_name in tags_list:
                        tag,created = Tag.objects.get_or_create(tag=tag_name)
                        infocomp.tags.add(tag)
                infocomp.last_modified = datetime.datetime.now()
                infocomp.thumbnail = None
                infocomp.save()
                return "You have successfully edited information composition " + infocomp.hash_key          
            else:
                response = rc.FORBIDDEN
                response.write(", You don't own this information composition so you can't modify data")
                return response
        else:
            data = request.data
            if not 'name' in data:
                response = rc.BAD_REQUEST
                response.write(", Name is required")   
                return response
            if not 'tags' in data:
                response = rc.BAD_REQUEST
                response.write(", Atleast one tag is required")
                return response 
            if not 'private' in data:
                private = False
            else:
                private = True
            if not 'description' in data:
                description = ""
            else:
                description = data['description'] 
            if not 'infocomp' in request.FILES:
                response = rc.BAD_REQUEST
                response.write(", Information Composition Icom file is required")
                return response
            infocomp = request.FILES["infocomp"]
            infocomp_filename = infocomp.name
            ext = os.path.splitext(infocomp_filename)[1]
            ext = ext.lower()
            if not ext == ".icom":
                response = rc.BAD_REQUEST
                response.write(", Please upload information Composition file, It should have icom extension")
                return response
            userid = request.session['_auth_user_id']
            user_obj = User.objects.get(pk=userid)
            infocomposition = InfoComposition.objects.create(                       
                 name = data['name'],
                 infocomp = infocomp,
                 description = description,
                 private = private,   
                 user = user_obj
                )
            tags = data["tags"]
            tags_list = tags.split(",")
            tags_final = []
            for tag in tags_list:
                tag = tag.lower().strip()
                tag = slugify(tag)
                tag = tag.replace("-","_")
                tags_final.append(tag)
            for tag_name in tags_list:
                tag,created = Tag.objects.get_or_create(tag=tag_name)
                infocomposition.tags.add(tag) 
            return "Information Composition Post successful!"
  

class LoginHandler(BaseHandler):
    allowed_methods = ('GET',)
    
    def read(self,request):
        response = rc.ALL_OK
        return response
     

class UserCompositionHandler(BaseHandler):
    allowed_methods = ('GET',)
        
    def read(self,request,username=None):
        if username:
            user_obj = get_object_or_404(User,username=username)          
            userid = user_obj.id
            infocomps = InfoComposition.objects.filter(user=userid,private=False)
            infocomp_list = list()
            for infocomp in infocomps:
                infocomp_list.append(UserDict(infocomp))   
            return infocomp_list
        else:
            userid = request.session['_auth_user_id']
            infocomps = infocomps = InfoComposition.objects.filter(user=userid)
            infocomp_list = list()
            for infocomp in infocomps:
                infocomp_list.append(UserDict(infocomp))
            return infocomp_list 
    
            
       
