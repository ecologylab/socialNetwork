from haystack.indexes import *
from haystack import site
from apps.infocomposition.models import *

class InfoCompositionIndex(SearchIndex):
    text = CharField(document=True,use_template=True)
    name = CharField(model_attr='name')     
    author = CharField(model_attr='user')
    description = CharField(model_attr="description")
    filename = CharField(model_attr="filename")  
    tags = MultiValueField()    

    
    def prepare_auther(self,obj):
        return obj.get_user_name()

   
    def prepare_tags(self,obj):
        return [tag.tag for tag in obj.tags.all()]
        
      
site.register(InfoComposition,InfoCompositionIndex)
