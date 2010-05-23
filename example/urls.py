from django.conf.urls.defaults import *

# Admin bit
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)

# Feedmap bit for recent users
from django.contrib.auth.models import User
from feedmap import feedmap

feedmap.register('users',
    User.objects.filter(is_active=True),
    date_field = 'date_joined',
    feed_attrs = {
        'title':'Recent Users',
        'link':'/users/',
        'description': 'People who joined the site recently'
    },
    priority = .9,
)

urlpatterns += feedmap.urls