from django.conf import settings
gettext = lambda s: s

# use django-notification if installed
FRIENDS_USE_NOTIFICATION_APP = getattr(settings,
                                       'FRIENDS_USE_NOTIFICATION_APP',
                                       True)

SHOW_FRIENDS_OF_FRIEND = getattr(settings,
                                'SHOW_FRIENDS_OF_FRIEND',
                                False)

NOTIFY_ABOUT_NEW_FRIENDS_OF_FRIEND = getattr(settings,
                                             'NOTIFY_ABOUT_NEW_FRIENDS_OF_FRIEND',
                                             False)

NOTIFY_ABOUT_FRIENDS_REMOVAL = getattr(settings,
                                       'NOTIFY_ABOUT_FRIENDS_REMOVAL',
                                       False)
