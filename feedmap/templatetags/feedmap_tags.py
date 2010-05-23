from django import template
from feedmap import feedmap,settings


register = template.Library()

def feedmeta(*args):
    """
    Renders HTML <link> tags for feeds (put within your <head> section)
    
    Usage:
        {% feedmeta [feeds,...] %}
    
    Example:
        {% load feedmap_tags %}
        
        {# Render all feed links #}
        {% feedmeta %}
        
        {# Render a set of given feeds #}
        {% feedmeta entries users %}
    """
    if len(args):
        return u''.join(map(feedmap.meta, args))
    return feedmap.metas
register.simple_tag(feedmeta)
   
class FeedListNode(template.Node):
    def __init__(self, *args):
        self.var = 'feed_list'
        if len(args) > 1 and args[-2] == 'as':
            self.var = args[-1]
        self.args = list(args)
    
    def render(self, context):
        context[self.var] = feedmap.feed_attrs.items()

def get_feed_lists(parser, token):
    """
    Places the requested feeds into a Context variable
    """
    return FeedListNode(*token.contents.split()[1:])
register.tag(get_feed_lists)

def get_feed_items(attrs):
    return attrs['items']('')
register.filter(get_feed_items)
    
def get_syn_links(name, format=''):
    from django.core.urlresolvers import reverse
    return reverse('feedmap_%s' % name, kwargs={'url':format})
register.filter(get_syn_links)
