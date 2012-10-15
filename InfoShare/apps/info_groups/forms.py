from django import forms
from apps.info_groups.models import *
from django.utils.safestring import mark_safe


class GroupForm(forms.ModelForm):
    
    Privacy = (
    ('0', mark_safe(u'<b>Open</b> &nbsp; | &nbsp; Anyone can see the group, who is in it and what members post.')),
    ('1', mark_safe(u'<b>Closed</b> &nbsp; | &nbsp; Anyone can see the group and who is in it. Only members see posts.')),
    ('2', mark_safe(u'<b>Secret</b> &nbsp; | &nbsp; Only members see the group, who is in it and what members post.')),    
    )

    name = forms.CharField(label="Name", help_text="Name of the group")
    privacy = forms.ChoiceField(label="Privacy",widget=forms.RadioSelect,choices=Privacy)   
 
    class Meta:
        model = Group
        exclude = ('users','hash_key')
