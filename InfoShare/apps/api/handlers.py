from piston.handler import BaseHandler
from apps.infocomposition.models import *
from django.shortcuts import get_object_or_404
from apps.api.utils import GetDict
from piston.utils import rc
from apps.infocomposition.models import InfoComposition
from django.contrib.auth.models import User

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

    def create(self,request):  
        if '_auth_user_id' in request.session:
            data = request.data
#           Testing, InfoComp model post will be implemented here
            return "Information Composition Post successful!"
        else:
            print("jainit")   
            response = rc.FORBIDDEN
            return response  



class LoginHandler(BaseHandler):
    allowed_methods = ('GET',)
    
    def read(self,request):
        response = rc.ALL_OK
        return response


     

