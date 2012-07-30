from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from apps.infocomposition.resource import UserAuthorization, CheckAuthentication, PrivateAuthorization
from tastypie.serializers import Serializer
from django.conf.urls.defaults import url
from django.contrib.auth.models import User
from apps.infocomposition.models import InfoComposition, Tag
from django.contrib.auth.models import User
from tastypie import fields

class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
	serializer = Serializer(formats=['xml'])

class TagResource(ModelResource):
        
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        serializer = Serializer(formats=['xml'])

	
class InfoCompositionResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    tags = fields.ManyToManyField(TagResource,"tags", full=True)
    
    class Meta:
        queryset = InfoComposition.objects.all()
        resource_name = 'infocomposition'
        authorization= PrivateAuthorization()
	authentication = CheckAuthentication()
	serializer = Serializer(formats=['xml'])
        excludes = ['id', 'infocomp','thumbnail']
        

    def dehydrate_filename(self, bundle):
        filename = bundle.data['filename'] + ".icom"
	return filename

    def dehydrate(self, bundle):
        username = bundle.obj.user
	bundle.data['username'] = username
        return bundle

class UserListResource(ModelResource):
    tags = fields.ManyToManyField(TagResource,"tags", full=True)
         
    class Meta:
        queryset = InfoComposition.objects.all()
        resource_name = 'userlist'
	authentication = CheckAuthentication()
	authorization = UserAuthorization()
	serializer = Serializer(formats=['xml'])
	default_format = "application/xml"
	excludes = ['id','infocomp', 'thumbnail']

    def dehydrate_filename(self, bundle):
        filename = bundle.data['filename'] + ".icom"
	return filename

    def dehydrate_resource_uri(self, bundle):
        pk = bundle.obj.id
        resource_url =  "/api/info/infocomposition" + "/" +  str(pk) + "/"
        return resource_url

