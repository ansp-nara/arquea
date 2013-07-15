#!/usr/bin/python

from django.core.management import setup_environ
import settings
setup_environ(settings)

from sys import path

path.append('/var/lib/admin')

from membro.models import Banco
from utils.functions import pega_bancos

novos = [b[0] for b in pega_bancos()]
antigos = [b.numero for b in Banco.objects.all()]

for banco in Banco.objects.all():
    if banco.numero not in novos:
        banco.delete()

for banco in pega_bancos():
    if banco[0] not in antigos:
        bb = Banco(numero=banco[0], nome=banco[1])
        bb.save()

