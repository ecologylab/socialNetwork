import kronos
from haystack.management.commands import update_index 


@kronos.register('*/1 * * * *')
def UpdateIndexItems():
    update_index.Command().handle()  
