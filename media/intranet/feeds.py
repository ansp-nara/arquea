from django.contrib.syndication.feeds import Feed
from cmsplugin_news.models import News
from django.utils.feedgenerator import Atom1Feed

class LatestNews(Feed):
    title = 'ANSP Grid Certification Authority News'
    link = '/'
    description = 'Updates on news'

    def items(self):
        return News.published.order_by('-pub_date')[:5]

    def item_link(self, item):
	return '/news/%s/%s/%s/%s' % (item.pub_date.strftime("%Y"),
				      item.pub_date.strftime("%m"),
				      item.pub_date.strftime("%d"),
                                      item.slug)

class AtomLatestNews(LatestNews):
    feed_type = Atom1Feed
    subtitle = LatestNews.description

