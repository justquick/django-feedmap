from django.conf import settings

# Base url to mount feeds on
FEED_BASE_URL = getattr(settings, 'FEED_BASE_URL', 'feeds/')

FEED_META_RSS = getattr(settings, 'FEED_META_RSS', True)
FEED_META_ATOM = getattr(settings, 'FEED_META_ATOM', True)

PUBLISHER = getattr(settings, 'SHARETHIS_PUBLISHER', 'PUT YOUR KEY HERE')
SENDS = getattr(settings, 'SHARETHIS_SENDS', ('email','sms','aim'))
POSTS = getattr(settings, 'SHARETHIS_POSTS', ('google_bmarks','facebook'))