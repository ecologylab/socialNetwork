import os
import zipfile
from django.db import models
from django.contrib.auth.models import User
from settings import MEDIA_ROOT


def get_upload_path(instance, filename):
    """
    To get upload path for specific user

    """
  
    userpath = "{name}/{file}".format(name=instance.user.username, file=filename)
    mainpath = "infocomp/" + userpath
    return mainpath



class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __unicode__(self):
        return self.tag

class InfoComposition(models.Model):
    """
    Main Information Composition Model   
    
    """

    name = models.CharField(max_length=50)
    infocomp = models.FileField(upload_to=get_upload_path)   
    tags = models.ManyToManyField(Tag, blank=True)
    description = models.TextField(blank=True)
    filename = models.CharField(max_length=50,blank=True)
    private = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User) 
  
    
    def __unicode__(self):
        return (u"Information composition uploaded by %s") % self.user
    
  
    def add_filename(self):
        infocomp_path = self.infocomp.name
        infocomp_base = os.path.basename(infocomp_path)        
        filename = os.path.splitext(infocomp_base)[0]
        self.filename = filename
        self.save()  

    def unzip_icom(self):
        infocomp_file = self.infocomp
        filename_with_ext = infocomp_file.name
        filename = os.path.splitext(filename_with_ext)[0]
        mainfile = zipfile.ZipFile(infocomp_file)        
        mainfile.extractall(MEDIA_ROOT + "/" +  filename)    
