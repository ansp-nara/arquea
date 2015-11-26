# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from monitor.models import Link


def grafico(request, link_id):
    link = get_object_or_404(Link, pk=link_id)

    return render_to_response('monitor/grafico.html', {'link': link})


def index(request):
    if request.user.is_authenticated():
        links = Link.objects.order_by('descricao')
    else:
        links = Link.objects.filter(fechado=False).order_by('descricao')
    return render_to_response('monitor/index.html', {'links': links})
