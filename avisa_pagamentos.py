#!/usr/bin/python

from django.core.management import setup_environ
import settings
setup_environ(settings)

from protocolo.models import Protocolo, Feriado
import datetime
from django.core.mail import send_mail

hoje = datetime.date.today()
d = datetime.timedelta(days=1)
prots = []

if Feriado.dia_de_feriado(hoje) or hoje.weekday() > 4:
    pass
else:
    prots += [p for p in Protocolo.objects.filter(data_vencimento=hoje)]
    pdia = hoje+d
    while Feriado.dia_de_feriado(pdia) or pdia.weekday()>4:
        prots += [p for p in Protocolo.objects.filter(data_vencimento=pdia)]
	pdia += d

    if len(prots) > 0:
        msg = ', '.join(['http://sistema.ansp.br/protocolo/protocolo/%s' % p.id for p in prots])
	send_mail("Protocolos a vencer hoje", "Os protocolos %s devem ser pagos hoje." % msg, "sistema@ansp.br", ["silvia@ansp.br"])
