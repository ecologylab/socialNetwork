from django.conf.urls.defaults import *


urlpatterns = patterns("friends.contrib.suggestions.views",

    url(r"^suggested_friends/$",
        "suggested_friends",
        name="friends_suggestions_suggested_friends"),

    url(r"^import_contacts/$",
        "import_contacts",
        name="friends_suggestions_import_contacts"),

    url(r"^import_google_contacts/$",
        "import_google_contacts",
        name="friends_suggestions_import_google_contacts"),

    url(r"^import_facebook_contacts/$",
        "import_facebook_contacts",
        name="friends_suggestions_import_facebook_contacts"),

    url(r"^import_twitter_contacts/$",
        "import_twitter_contacts",
        name="friends_suggestions_import_twitter_contacts"),

    url(r"^import_yahoo_contacts/$",
        "import_yahoo_contacts",
        name="friends_suggestions_import_yahoo_contacts"),

    url(r"^import_linkedin_contacts/$",
        "import_linkedin_contacts",
        name="friends_suggestions_import_linkedin_contacts"),

    url(r"^oauth_access/", include("oauth_access.urls")),

)
