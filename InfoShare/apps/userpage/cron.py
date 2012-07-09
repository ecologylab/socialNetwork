import django
import kronos

@kronos.register('*/1 * * * *')
def SendMail():
    django.core.management.call_command("send_mail")
    
@kronos.register('*/1 * * * *')
def RetryMail():
    django.core.management.call_command("retry_deferred")

    

    
