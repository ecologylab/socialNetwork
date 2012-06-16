from django.db.models import get_models, signals
from django.conf import settings
from django.utils.translation import ugettext_noop as _

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("Picture_updated", _("Picture_updated"), _("You have successfully updated your profile picture"), default=1)
        notification.create_notice_type("Picture_added", _("Picture_added"), _("You have successfully added new profile picture"), default=1)
    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"

