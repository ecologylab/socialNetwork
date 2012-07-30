from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from django.contrib.auth.models import User

class UserAuthorization(Authorization):

    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(user=request.user.id)
        return object_list.none()

class CheckAuthentication(BasicAuthentication):
    def __init__(self, *args, **kwargs):
        super(CheckAuthentication, self).__init__(*args, **kwargs)

    def is_authenticated(self, request, **kwargs):
        from django.contrib.sessions.models import Session
#	print(request.COOKIES)
#	print(request.user)
        if 'sessionid' in request.COOKIES:
            s = Session.objects.get(pk=request.COOKIES['sessionid'])
            if '_auth_user_id' in s.get_decoded():
		u = User.objects.get(id=s.get_decoded()['_auth_user_id'])
                request.user = u
                return True
        return super(CheckAuthentication, self).is_authenticated(request, **kwargs)

class PrivateAuthorization(Authorization):
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
	    public_obj = object_list.filter(private=False)
	    user_obj = object_list.filter(user=request.user.id)
	    final_obj = public_obj | user_obj
	    return final_obj	    
	return object_list.none()
