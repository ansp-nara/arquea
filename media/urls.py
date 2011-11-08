from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from cms.sitemaps import CMSSitemap
from intranet.views import PageSearchView

admin.autodiscover()

admin.site.root_path = "/admin/" # there is probably a bug in django...

urlpatterns = patterns('',
    #(r'^admin/(.*)', admin.site.root),
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'cmspages': CMSSitemap}}),
    (r'^admin/', include(admin.site.urls)),
    (r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
    (r'^categories/', include('categories.urls')),
    (r'^intranet/', include('intranet.urls')),
    (r'^isms/', include('isms.urls')),
    (r'^photologue/', include('photologue.urls')),
    (r'^accounts/login/$', 'django_cas.views.login'),
    (r'^accounts/logout/$', 'django_cas.views.logout'),
    (r'^login$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
#    (r'^search/', include('haystack.urls')),

)
urlpatterns += patterns('haystack.views',
    url(r'^search/$', PageSearchView(), name='haystack_search'),
)

if settings.DEBUG:
    urlpatterns+= patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'^media_admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/var/www/media_admin', 'show_indexes': True})
    )

urlpatterns += patterns('',
    url(r'^', include('cms.urls')),
)
