# -*- coding: utf-8 -*-
#!/usr/bin/python

from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
a = UserManager()

from django.contrib.auth.models import Group
pes = Group.objects.get(name='pesquisa')

to_change = []
users = open('laboratorios')
for u in users:
    dd = u.split(';')
    dd[4] = (pes,)
    to_change.append(dd)
#to_change.append(['teste', 'Teste', 'do Teste', 'antonio@ansp.br', (c2,p1)])
#to_change.append(['lopez', 'Luis Fernandez', 'Lopez', 'lopez@dim.fm.usp.br', (c2, p1)])
#to_change.append(['yamamoto', 'Jorge', 'Yamamoto', 'yamamoto@ansp.br', (c2, p1)])
#to_change.append(['clarice', 'Clarice', '', 'clarice@ansp.br', (c2, p1)])
#to_change.append(['anna', 'Anna Paula', 'Costa', 'anna@ansp.br', (c2, p1)])
#to_change.append(['douglas', 'Douglas', 'Azullini', 'douglas@ansp.br', (c2, p2)])
#to_change.append(['jrgmrcs', 'Jorge Marcos', 'de Almeida', 'jrgmrcs@ansp.br', (c2,)])
#to_change.append(['marcio', 'Marcio', 'Costa', 'marcio@ansp.br', (c2,)])
#to_change.append(['sheila', 'Sheila', 'Souza', 'sheila@ansp.br', (c1,)])
#to_change.append(['silvia', 'Silvia', 'Cruz', 'silvia@ansp.br', (p1,c2)])
#to_change.append(['renato', 'Renato', 'Souza', 'renato@ansp.br', (c1,)])
#to_change.append(['carlos', 'Carlos', 'Ribas', 'carlos@ansp.br', (c1,)])
#to_change.append(['greice', 'Greice', 'Munhoz', 'greice@ansp.br', (c1,)])
#to_change.append(['teste11', 'Renato', 'Teste1', 'renato@ansp.br', (pes,)])
#to_change.append(['teste12', 'Antonio', 'Teste2', 'antonio@ansp.br', (pes,)])
#to_change.append(['teste1', 'Teste', 'da Silva', 'antonio@ansp.br', (c2, p1)])
#to_change.append(['teste2', 'Teste 2', 'de Souza', 'antonio@ansp.br', (c1,)])


from smtplib import SMTP
smtp_c = SMTP('mail.ansp.br')
fromchanger = 'yamamoto@ansp.br'
msg = u'Subject: Pesquisa sobre a rede KyaTera\nTo:%s %s <%s>\nFrom:Jorge Yamamoto <yamamoto@ansp.br>\nContent-Type: text/plain; charset="utf-8"\n\n%s'
txt_f = open('texto_pesquisa.txt')
txt = txt_f.read()

for u in to_change:
    user = User(username=u[0], first_name=u[1], last_name=u[2], email=u[3], is_staff=True, is_active=True)
    pwd = a.make_random_password()
    user.set_password(pwd)
    user.save()
    for p in u[4]:
       user.groups.change(p)
    msg2 = msg % (u[1],u[2], u[3], txt)
    smtp_c.sendmail(fromchanger, u[3], msg2 % (u[0], pwd))
   