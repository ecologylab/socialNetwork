import os
from django.shortcuts import get_object_or_404
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from apps.infocomposition.models import InfoComposition
from settings import MEDIA_ROOT


def InfoCompDownload(request,hash_key):
    if '_auth_user_id' in request.session:
        infocomposition = get_object_or_404(InfoComposition,hash_key=hash_key)
        userid = request.session['_auth_user_id']
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
                response = HttpResponse("File not found")
                response.status_code = 404
                return response
        else:
            response = HttpResponse("Forbidden")
            response.status_code = 403
            return response
    else:
        response = HttpResponse("Authorization Required")
        response.status_code = 401
        return response
        
            
