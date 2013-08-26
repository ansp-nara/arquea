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
p2 = Group.objects.get(name='protocolo_add')
c1 = Group.objects.get(name='comite')
c2 = Group.objects.get(name='contatos_add')

to_add = []
#to_add.append(['teste122345', 'Paulo', 'Santos', 'antonio@ansp.br', (c1,)])
#to_add.append(['teste122346', 'Ronaldo', 'Melare', 'ajoaoff@gmail.com', (c1,)])
to_add.append(['wagner', 'Wagner', '', 'wagner@dca.fee.unicamp.br', (c1,)])
to_add.append(['anzaloni', 'Alessandro', 'Anzaloni', 'anzaloni@ita.br', (c1,)])
to_add.append(['maah', 'Marco', 'Henriques', 'maah@unicamp.br', (c1,)])
to_add.append(['paulopaiva', 'Paulo', 'Bandiera Paiva',  'paiva@unifesp.br', (c1,)])
to_add.append(['regina', 'Regina', '', 'regina@ufscar.br', (c1,)])
to_add.append(['carvalho', 'Tereza Cristina', 'M. B. Carvalho', 'carvalho@larc.usp.br', (c1,)])
to_add.append(['irenilce', 'Maria Irenilce', 'Marinheiro', 'MIM1@fapesp.br', (c1,)])

#from smtplib import SMTP
#smtp_c = SMTP('10.0.1.3')
#fromaddr = 'sistema@ansp.br'
msg = u'Prezado %s %s, membro do Comitê Gestor da Rede ANSP.\n\nSeu usuário no sistema administrativo da ANSP (https://sistema.nara.org.br) foi criado com sucesso.\nSeu login é %s e sua senha %s. Solicitamos que a senha inicial seja alterada o mais breve possível, clicando em "Alterar senha", no canto superior direito da tela, logo após o login.\n\nAtenciosamente\nAntonio João F. Francisco\nAnalista de Sistemas Sênior\nPrograma Rede ANSP/FAPESP'


for u in to_add:
    user = User(username=u[0], first_name=u[1], last_name=u[2], email=u[3], is_staff=True, is_active=True)
    pwd = a.make_random_password()
    user.set_password(pwd)
    user.save()
    for p in u[4]:
        user.groups.add(p)
    print msg % (u[1],u[2],u[0],pwd)
    print
    print


