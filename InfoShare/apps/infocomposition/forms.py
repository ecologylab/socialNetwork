import os
from django import forms
from apps.infocomposition.models import *
from django.template.defaultfilters import slugify

class InfoForm(forms.ModelForm):

    infocomp = forms.FileField(label="Information Composition", help_text="Add .icom Information composition File")
    tags = forms.CharField(label=u"Tags", help_text="Add tags, separate them with comma")     
 
    class Meta:
        model = InfoComposition
        exclude = ('user','filename','thumbnail')
     
    def clean_infocomp(self):
        infocomp = self.cleaned_data['infocomp']
        filename = infocomp.name
        ext = os.path.splitext(filename)[1]        
        ext = ext.lower() 
        if not ext == ".icom":
            raise forms.ValidationError("Pleae upload a Information composition icom file") 
        else:
            infocomp.name = filename.replace(" ","_")
            return infocomp
     
    def clean_tags(self):
        tags = self.cleaned_data['tags']     
        tags_list = tags.split(",")
        tags_final = []
        for tag in tags_list:
            tag = tag.lower().strip()
            tag = slugify(tag)
            tags_final.append(tag)
        return tags_final
  
class EditForm(forms.Form):
  
    tags = forms.CharField(label=u"Tags", help_text="Add tags, separate them with comma")     
 
    class Meta:
        model = InfoComposition
        exclude = ('user','filename','infocomp','thumbnail')
      
 
    

   
