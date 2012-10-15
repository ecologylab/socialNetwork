import random
import string
from django.db import models
from django.contrib.auth.models import User



def get_random_hash():
    """ Get random unique hash """

    pool = string.letters + string.digits
    rand_string =  ''.join(random.choice(pool) for i in xrange(10))
    exists = True
    while(exists == True):
        try:
            obj = get_object_or_404(Group,hash_key=rand_string)
            rand_string =  ''.join(random.choice(pool) for i in xrange(10))
        except:            
            exists = False
    return rand_string
            

class Group(models.Model):
    """
    Main Groups model 

    """
    
    Privacy = (
    ('0','Open'),
    ('1','Closed'),
    ('2','Secret')
    )
   
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User,through="GroupUser")
    privacy = models.CharField(max_length=10,choices=Privacy)
    created = models.DateTimeField(auto_now_add=True)    
    hash_key = models.CharField(max_length=10,null=True,unique=True)    

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'group'
        verbose_name_plural = 'groups'

    def save(self, *args,**kwargs):
        if not self.hash_key:
            self.hash_key = get_random_hash()
        super(Group,self).save(*args,**kwargs)
    

    def add_user(self,user,is_admin=False):
        return GroupUser.objects.create(user=user,group=self,is_admin=is_admin)

    def is_member(self,user):
        return True if user in self.users.all() else False

    def is_admin(self,user):
        return True if self.group_users.filter(user=user,is_admin=True) else False

    def get_admins(self):
        return self.group_users.filter(is_admin=True)

class GroupUser(models.Model):
    """
    Model for members associated with perticular group

    """

    user = models.ForeignKey(User,related_name="group_users")
    group = models.ForeignKey(Group,related_name="group_users")
    is_admin = models.BooleanField(default=False)

    class Meta:
        ordering = ['group','user']
        unique_together = ('user','group')
        verbose_name = "group user"
        verbose_name_plural = "group users"
 
    def __unicode__(self):
        return u"{0}: {1}".format(self.user.username, self.group)

    def delete(self):
        if len(self.group.get_admins()) == 1 and self.is_admin == True:
            raise Exception("There should be atleast one owner of the group")
        else:
            super(GroupUser,self).delete()


