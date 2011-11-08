from django.conf.urls.defaults import *
from feeds import LatestNews, AtomLatestNews

feeds = {'rss': LatestNews,
	 'atom': AtomLatestNews}

urlpatterns = patterns('intranet.views',
    (r'^$', 'sample_view', {'message': 'urls.py => root (DE)',}),
    (r'^$', 'sample_view', {'message': 'urls.py => root (EN)'}),
    (r'^login$', 'login'),
    (r'^logout$', 'logout'),
    (r'^agenda/$', 'agenda'),
    (r'^agenda/(?P<char>.)/$', 'agenda'),
    (r'^agenda/(?P<char>.)/(?P<pess>.+)/$', 'agenda'),
    (r'^membros/$', 'membros'),
    (r'^membros/(?P<class_id>\d+)/$', 'membros'),
    (r'^custeio/(?P<tipo>.+)$', 'custeio'),
    (r'^ferias$', 'ferias'),
    (r'^(?P<termo_id>\d+)/barra.png$', 'grafico_barra'),
    (r'^(?P<termo_id>\d+)/pizza.png$', 'grafico_pizza'),
    (r'^(?P<mod_id>\d+)/modalidade.png$', 'barra_modalidades'),
    (r'^(?P<a_id>\d+)/acordo.png$', 'barra_acordos'),
    (r'^(?P<a_id>\d+)/ac_mod.png$', 'linhas_ac_mod'),
    (r'^resumo_termo$', 'resumo_termo'),
    (r'^modalidades$', 'tempo_modalidade'),
    (r'^acordo_modalidades$', 'acordo_modalidades'),
    (r'^modalidadesmap$', 'tempo_modalidade2'),
    (r'^acordos$', 'tempo_acordo'),
    (r'^modalidades(?P<acima>\d).png$', 'linha_modalidades'),
    (r'^(?P<termo_id>\d+)/teste$', 'grafico_pizza_teste2'),
    (r'^(?P<termo_id>\d+)/coluna$', 'grafico_coluna_teste'),

    url(r'^sublevel$', 'sample_view', kwargs={'message': 'urls.py => sublevel'}, name='sample-app-sublevel'),
)
urlpatterns += patterns('', (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),)
