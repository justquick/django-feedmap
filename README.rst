Feedmap
=======

:Authors:
   Justin Quick <justquick@gmail.com>
:Version: 0.1

::

    pip install django-feedmap

Django Feedmap is a syndication feeds and sitemaps generator for django.
Register the querysets only once with feedmap so it knows how to populate
the feeds. Put this bit in your urls.py::
    
    from feedmap import feedmap

    feedmap.register('entries',
        BlogEntry.objects.filter(is_public=True),
        feed_attrs = {
            'title':'Recent Blog Entries',
            'link':'/blog/',
        },
    )
    
    urlpatterns += feedmap.urls

Then it will generate syndication feeds in atom and rss2 formats as well as corresponding sitemaps::

    /sitemap.xml # Global Index
    /sitemap-feeds.xml # Index of syndication feeds
    /sitemap-entries.xml # Actual sitemap of recent blog entries
    /feeds/entries # RSS2 feed
    /feeds/entries/atom # Atom feed
    
