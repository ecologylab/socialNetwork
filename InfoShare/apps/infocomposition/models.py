import os
import glob
import zipfile
from shutil import rmtree
from tempfile import *
from math import log
from PIL import Image as PImage
from mptt.models import MPTTModel, TreeForeignKey
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
    

    def tagcloud(self):

        counts, taglist, tagcloud = [], [], []
                
        threshold=0  # Threshold occurence value, i.e,  0 means minimum size with no occurrence
        maxsize=2.5   # Maximum css size
        minsize=1  # Minimum css size
        
        tags = Tag.objects.all()
        for tag in tags:
            count = tag.infocomposition_set.count()
            count >= threshold and (counts.append(count), taglist.append(tag))
            
        maxcount = max(counts)
        mincount = min(counts)
        constant = log(maxcount - (mincount - 1))/(maxsize - minsize or 1)
        tagcount = zip(taglist, counts)
        if constant == 0:
            constant = 1
        for tag, count in tagcount:
            size = log(count - (mincount - 1))/constant + minsize
            tagcloud.append({'tag': tag, 'id': tag.id, 'count': count, 'size': round(size, 7)})
        return tagcloud


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
        return (u"Information composition %s") % self.name

    def get_user_name(self):
        return self.user
  
    class Meta:
        ordering = ('-added',)   
  
    def save(self,*args,**kwargs):
        infocomp_path = self.infocomp.name
        infocomp_base = os.path.basename(infocomp_path)        
        filename = os.path.splitext(infocomp_base)[0]
        self.filename = filename	
        super(InfoComposition,self).save(*args,**kwargs)
	if not self.thumbnail:
            self.unzip_and_generate()
	   

    def unzip_and_generate(self):
        infocomp_file = self.infocomp
        filename_with_ext = infocomp_file.name
        filename = os.path.splitext(filename_with_ext)[0]    
        file_base = os.path.basename(filename)
        mainfile = zipfile.ZipFile(infocomp_file)        
        mainfile.extractall(MEDIA_ROOT + "/" +  filename) 
        mainfile.close()
        infocomp_dir = os.path.join(MEDIA_ROOT,filename) 
        os.chdir(infocomp_dir)
        file_list = glob.glob("*.jpg")
        length = len(file_list)
        if length > 1:
            for name in file_list:
                if not name.endswith("_thumbnail.jpg"):
                    image_name = name                 
        elif length == 1:
            image_name = file_list[0] 
        else:
            pass
                    
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
        infocomp_dir_path = os.path.splitext(infocomp_name)[0]
        infocomp_path = os.path.join(MEDIA_ROOT,infocomp_name)              
        infocomp_dirpath = os.path.join(MEDIA_ROOT,infocomp_dir_path)
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

class Comment(MPTTModel):
    """
    Threaded comments 
  
    """
    infocomp = models.ForeignKey(InfoComposition)
    author = models.CharField(max_length=60)
    comment = models.TextField()
    added  = models.DateTimeField()
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by=['added']

