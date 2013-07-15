# -*- coding: utf-8 -*-
#!/usr/bin/python

from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
a = UserManager()

from django.contrib.auth.models import Group
p1 = Group.objects.get(name='protocolo')
p2 = Group.objects.get(name='protocolo_change')
c1 = Group.objects.get(name='contatos')
c2 = Group.objects.get(name='contatos_change')

to_change = []
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
to_change.append(['paulo', 'Paulo', 'Santos', 'pccs@dim.fm.usp.br', (c1,)])
to_change.append(['ronaldo', 'Ronaldo', 'Melare', 'ronaldo@ansp.br', (c1,)])
#to_change.append(['teste1', 'Teste', 'da Silva', 'antonio@ansp.br', (c2, p1)])
#to_change.append(['teste2', 'Teste 2', 'de Souza', 'antonio@ansp.br', (c1,)])


from smtplib import SMTP
smtp_c = SMTP('mail.ansp.br')
fromchanger = 'sistema@ansp.br'
msg = u'Subject: Senha do sistema administrativo\nTo:%s %s <%s>\nContent-Type: text/plain; charset="utf-8"\n\nOlá, %s %s.\n\nSeu usuário no sistema administrativo do NARA (https://sistema.nara.org.br/admin) foi criado com sucesso.\nSeu login é %s e sua senha %s. Solicitamos que a senha inicial seja alterada o mais breve possível, clicando em "Alterar senha", no canto superior direito da tela, logo após o login.\n\nAtenciosamente\nAdministração do sistema'


for u in to_change:
    user = User(username=u[0], first_name=u[1], last_name=u[2], email=u[3], is_staff=True, is_active=True)
    pwd = a.make_random_password()
    user.set_password(pwd)
    user.save()
    for p in u[4]:
        user.groups.change(p)
    smtp_c.sendmail(fromchanger, u[3], msg % (u[1],u[2], u[3], u[1],u[2],u[0],pwd))