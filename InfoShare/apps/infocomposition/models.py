import os
import zipfile
from shutil import rmtree
from tempfile import *
from PIL import Image as PImage
from django.db import models
from django.core.files import File
from django.contrib.auth.models import User
from settings import MEDIA_ROOT


def get_upload_path(instance, filename):
    """
    To get upload path for specific user

    """
  
    userpath = "{name}/{file}".format(name=instance.user.username, file=filename)
    mainpath = os.path.join("infocomp",userpath)
    return mainpath


def thumbnail_path(instance, filename):
    """
    thumbnail path for user
    
    """
    
    username = instance.user.username
    mainpath = os.path.join("infocomp",username,"thumbnails",filename)
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
    thumbnail = models.ImageField(upload_to=thumbnail_path, blank=True, null=True)
    
    
    def __unicode__(self):
        return (u"Information composition uploaded by %s") % self.user
    
  
    def save(self,*args,**kwargs):
        infocomp_path = self.infocomp.name
        infocomp_base = os.path.basename(infocomp_path)        
        filename = os.path.splitext(infocomp_base)[0]
        self.filename = filename
        super(InfoComposition,self).save(*args,**kwargs)

    def unzip_and_generate(self):
        infocomp_file = self.infocomp
        filename_with_ext = infocomp_file.name
        filename = os.path.splitext(filename_with_ext)[0]
        file_base = os.path.basename(filename)
        mainfile = zipfile.ZipFile(infocomp_file)        
        mainfile.extractall(MEDIA_ROOT + "/" +  filename) 
        image_name = file_base + ".jpg" 
        image_path = os.path.join(MEDIA_ROOT,filename,image_name)
        if os.path.isfile(image_path):                                  # Generate thumbnail if jpeg file exists
            im = PImage.open(image_path)
            im.thumbnail((256,256), PImage.ANTIALIAS)
            thumb_file = file_base + "-thumb" + ".jpg"
            tf = NamedTemporaryFile()
            im.save(tf.name, "JPEG")
            self.thumbnail.save(thumb_file, File(open(tf.name)), save=False)
            tf.close()
            self.save()

       
    def delete(self): 
        infocomp_name = self.infocomp.name
        user_id = self.user_id
        user_object = User.objects.get(pk=user_id)     
        user_name = user_object.username
        infocomp_with_ext = os.path.basename(infocomp_name)
        infocomp_file = os.path.splitext(infocomp_with_ext)[0]
        infocomp_path = os.path.join(MEDIA_ROOT,infocomp_name)              
        infocomp_dirpath = os.path.join(MEDIA_ROOT,"infocomp",user_name,infocomp_file)
        thumb_path = os.path.join(MEDIA_ROOT,self.thumbnail.name)
             
        # Delete .icom file, if exists
        if os.path.isfile(infocomp_path):
            os.remove(infocomp_path)
       
        # Delete extracted directory, if exists
        if os.path.isdir(infocomp_dirpath): 
            rmtree(infocomp_dirpath)

        # Delete thumbnail, if exists
        if os.path.isfile(thumb_path):
            os.remove(thumb_path)
        
        super(InfoComposition,self).delete()
