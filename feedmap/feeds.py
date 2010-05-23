from django.contrib.sitemaps import  GenericSitemap
from django.conf.urls.defaults import patterns,url
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from django.core.exceptions import FieldError
from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site
from django.db.models.query import QuerySet
import settings

class FeedMap(object):
    """
    Syndication Feeds & Sitemaps Generator
    """
    feed_attrs = {}
    sitemaps = {
        'feeds': GenericSitemap({
            'queryset':Site.objects.all() # Give it some model
        })
    }
    
    def register(self, feedname, queryset=None, model=None, lookup=None, date_field=None, feed_attrs={}, **sitemap_attrs):
        """
        Register a named queryset, give a date_field to order by, and any extra attrs you want
        
        the name is where it will be located in your feeds
        feed_attrs (ie description,subtitle,etc) will be passed into the Feed generator
        sitemap_attrs (ie priority) will be passed into the GenericSitemap generator
        """
        assert isinstance(queryset, QuerySet) or (model and not lookup is None)
        if isinstance(queryset, QuerySet):
            model = queryset.model
        else:
            queryset = model.objects.filter(**lookup)
        date_field = date_field or model._meta.get_latest_by
        assert bool(date_field), "register() requires either a date_field parameter or 'get_latest_by' in the model"
        def orderer(_):
            try:
                return queryset.order_by('-%s' % date_field)
            except FieldError:
                return queryset
        feed_attrs.update({
            'items': orderer,#lambda _: queryset.order_by('-%s' % date_field),
            'title': feed_attrs.pop('title', feedname.title()),
            'model': model,
        })
        self.feed_attrs[feedname] = feed_attrs
        attrs = {'queryset':queryset}
        if date_field:
            attrs['date_field'] = date_field
        self.sitemaps[feedname] = GenericSitemap(attrs, **sitemap_attrs)
        
        
    def author(self, feedname=None, **kwargs):
        """
        Author a given feed with author_* info
        
        if no feedname, all feeds are authored
        kwargs are part after author_ (name,link,email)
        """
        kwargs = dict((('author_%s' % k, v) for k,v in kwargs.items()))
        if feedname is None and kwargs:
            for value in self.feed_attrs.values():
                value.update(kwargs)
        elif feedname in self.feed_attrs and kwargs:
            self.feed_attrs[feedname].update(kwargs)
    
    def meta(self, name):
        """
        Retrieve HTML <link> for a given feed
        """
        def helper(syntype):
            return u'<link rel="alternate" title="%s: %s" href="%s" type="application/%s+xml">' % (
                syntype.title(), self.feed_attrs[name]['title'],
                self.get_feed_url(name, syntype), syntype,
            )
        if settings.FEED_META_ATOM and settings.FEED_META_RSS:
            return u''.join((helper('rss'),helper('atom')))
        elif settings.FEED_META_ATOM:
            return helper('atom')
        elif settings.FEED_META_RSS:
            return helper('rss')
        return u''
        
    @property
    def metas(self):
        """
        Return all HTML <link> tags in this sitemap
        """
        return u''.join(map(self.meta, self.feed_attrs))
    
    def get_feed_url(self, name='',syntype=''):
        return 'http://%s/%s%s/%s' % (
            Site.objects.get_current().domain,
            settings.FEED_BASE_URL, name, syntype
        )

    def feed_factory(self, name, attrs):
        """
        Generate Syndication feeds of set format
        """
        attrs.update({'feed_type':Rss201rev2Feed})
        rss = type('Rss%s' % name, (Feed,), attrs)
        attrs.update({'feed_type':Atom1Feed})
        atom = type('Atom%s' % name, (Feed,), attrs)
        
        if settings.FEED_META_ATOM and settings.FEED_META_RSS:
            return {'rss':rss,'':rss,'atom':atom}
        elif settings.FEED_META_ATOM:
            return {'':atom,'atom':atom}
        elif settings.FEED_META_RSS:
            return {'rss':rss,'':rss}
        return {}
        
    @property
    def urls(self):
        """
        Compute Sitemap + Feed URLs and return patterns
        """
        
        smfeeds = []
        if settings.FEED_META_RSS:
            smfeeds.extend(map(self.get_feed_url, self.feed_attrs))
        if settings.FEED_META_ATOM:
            smfeeds.extend(map(lambda u: u'%satom' % u, smfeeds))
        
        for name in self.feed_attrs:
            self.feed_attrs[name]['feed_url'] = self.get_feed_url(name)
        
        return patterns('django.views.generic.simple',
            (r'^sitemap-feeds.xml$', 'direct_to_template', {
                'template':'sitemap_index.xml', 'mimetype': 'application/xml',
                'extra_context': { 'sitemaps': smfeeds }
            })
        ) + \
        patterns('django.contrib.sitemaps.views', 
            (r'^sitemap.xml$', 'index', {'sitemaps': self.sitemaps}),
            (r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {
                'sitemaps': self.sitemaps
            }),
        ) + \
        patterns('django.contrib.syndication.views', *( url(
                r'^%s%s/(?P<url>.*)' % (settings.FEED_BASE_URL, name), 'feed', {
                    'feed_dict': self.feed_factory('%sFeed' % name.title(), value)
                }, name='feedmap_%s' % name
            ) for name,value in self.feed_attrs.items())
        )
        
feedmap = FeedMap()