from django.conf.urls import *

urlpatterns = patterns('configuracao.views',
    (r'^help/(\w+)/(\w+)/$','help_text' ),
)

